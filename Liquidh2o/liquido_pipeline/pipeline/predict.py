import numpy as np, pandas as pd, os, yaml, joblib
from sqlalchemy import create_engine, text
from .features import make_time_features
from .utils_sql import load_by_tanks, write_table
import argparse
import os, argparse, yaml, joblib, numpy as np, pandas as pd
from sqlalchemy import create_engine, text
from .features import make_time_features
from .model_utils import load_artifact
import warnings
warnings.filterwarnings("ignore", message="X does not have valid feature names")


def predict_batch(db_engine, cfg_path="config/tanks_predict.yaml",
                  limit=None, tanks_arg=None, dry_run=False, model_ver="lgbm_v1"):
    import yaml, numpy as np, pandas as pd
    from sqlalchemy import text
    from .features import make_time_features
    from .utils_sql import load_by_tanks, write_table
    from .model_utils import load_artifact

    # --- load config
    cfg = yaml.safe_load(open(cfg_path, "r", encoding="utf-8"))
    base, sch = cfg["tables"]["base"], cfg["tables"]["base_schema"]
    out_table, out_schema = cfg["tables"]["preds"], cfg["tables"]["schema"]
    ts, y, g = cfg["general"]["ts_col"], cfg["general"]["target"], cfg["general"]["group_col"]
    use_log_default = bool(cfg["general"].get("log_target", True))
    registry = cfg["paths"]["registry"]

    # --- tanks list
    tanks = cfg["groups"]["individual"] + cfg["groups"].get("complex", [])
    if tanks_arg:
        tanks = [int(x) for x in tanks_arg.split(",")]
    if limit:
        tanks = tanks[:limit]

    out_rows = []

    for tid in tanks:
        art = load_artifact(registry, f"tank_{tid}")
        print(f"[predict] tank_{tid} artifact? {bool(art)}")
        if not art:
            print(f"⏭️  Skipping tank {tid}: no artifact found.")
            continue

        # prefer per-artifact log flag if present
        use_log = bool(art.get("meta", {}).get("log_target", use_log_default))

        df = load_by_tanks(db_engine, base, [tid], schema=sch, ts_col=ts)
        print(f"[predict] tank {tid}: loaded rows={len(df)} from {sch}.{base}")
        if df.empty:
            print(f"⏭️  Skipping tank {tid}: no data in view.")
            continue

        # ensure datetime + sort
        df[ts] = pd.to_datetime(df[ts], errors="coerce")
        df = df.dropna(subset=[ts]).sort_values(ts)

        # build features, split hist (target present) vs fut (target null)
        dff  = make_time_features(df, target=y, group_cols=[g], ts_col=ts)
        hist = dff[dff[y].notna()].copy()
        fut  = dff[dff[y].isna()].copy()
        print(f"[predict] tank {tid}: hist={len(hist)} fut={len(fut)} (use_log={use_log})")

        if hist.empty or fut.empty:
            print(f"⏭️  Skipping tank {tid}: need past+future rows (NULL target for future).")
            continue

        expected = art.get("features", None)
        if not expected or len(expected) == 0:
            raise RuntimeError(f"Artifact for tank_{tid} is missing 'features'. Retrain to save features list.")

        # recursive step-ahead
        series = hist.set_index(ts)[y].copy()

        for _, r in fut.iterrows():
            # base row with static/time features for the future timestamp
            base_row = fut.loc[fut[ts] == r[ts], expected].copy()
            if base_row.empty:
                base_row = pd.DataFrame({c: [np.nan] for c in expected})
            # recompute lag/rolling features from history + predictions so far
            tmp = pd.concat(
                [hist[[ts, g, y]], pd.DataFrame({ts: [r[ts]], g: [r[g]], y: [np.nan]})],
                ignore_index=True
            ).sort_values(ts)
            tmp[y] = tmp[ts].map(series)
            lag_row = make_time_features(tmp, target=y, group_cols=[g], ts_col=ts).tail(1)

            # inject available lag cols
            lag_cols = [c for c in lag_row.columns if c in expected]
            for c in lag_cols:
                base_row.loc[:, c] = lag_row[c].values[0]

            # ensure exact training column order
            for c in expected:
                if c not in base_row.columns:
                    base_row.loc[:, c] = np.nan
            ft = base_row[expected]

            # transform & predict
            X = art["prep"].transform(ft)
            pred = float(art["model"].predict(X)[0])
            # unlog if necessary
            pred_before = pred
            if use_log:
                pred = float(np.expm1(pred))
            # optional clamp if capacity is present
            cap = float(df["capacity"].iloc[0]) if "capacity" in df.columns and pd.notna(df["capacity"].iloc[0]) else None
            if cap is not None:
                pred = float(np.clip(pred, 0, cap))

            out_rows.append((int(r[g]), r[ts], pred, model_ver))
            # feed back for next step
            series.loc[r[ts]] = pred

        # quick per-tank summary
        print(f"[predict] tank {tid}: wrote {sum(1 for _ in fut.iterrows())} future steps")

    # assemble
    if not out_rows:
        print("[predict] nothing to write")
        return pd.DataFrame(columns=[g, ts, "median_level_pred", "model_ver"])

    out = pd.DataFrame(out_rows, columns=[g, ts, "median_level_pred", "model_ver"])

    # human check
    try:
        print(out.groupby(g)[ts].agg(["min","max","count"]).reset_index().head(20))
    except Exception:
        pass

    if dry_run:
        print("DRY RUN: not writing to DB. Rows:", len(out))
        return out

    # upsert using YAML table/schema
    print(f"[predict] upserting {len(out)} rows into {out_schema}.{out_table}")
    records = out.rename(columns={g: "tank_id", ts: "updated_at"}).to_dict("records")
    CHUNK = 10000
    with db_engine.begin() as con:
        for i in range(0, len(records), CHUNK):
            con.execute(text(f"""
                INSERT INTO {out_schema}.{out_table} (tank_id, updated_at, median_level_pred, model_ver)
                VALUES (:tank_id, :updated_at, :median_level_pred, :model_ver)
                ON CONFLICT (tank_id, updated_at)
                DO UPDATE SET median_level_pred = EXCLUDED.median_level_pred,
                              model_ver  = EXCLUDED.model_ver
            """), records[i:i+CHUNK])
            print(f"[predict] upserted {min(i+CHUNK, len(records))}/{len(records)} rows")

    return out




def make_engine():
    pg_user = os.getenv("PGUSER", "postgres")
    pg_pass = os.getenv("PGPASSWORD", "postgres")
    pg_host = os.getenv("PGHOST", "localhost")
    pg_port = os.getenv("PGPORT", "5432")
    pg_db   = os.getenv("PGDATABASE", "liquidosep")
    return create_engine(f"postgresql+psycopg2://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}")

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cfg", default="config/tanks_predict.yaml")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--tanks", type=str, default=None)  # "31,69"
    ap.add_argument("--model-ver", type=str, default="lgbm_v1")
    return ap.parse_args()

def main():
    args = parse_args()
    engine = make_engine()
    out = predict_batch(engine,
                        cfg_path=args.cfg,
                        model_ver=args.model_ver,
                        limit=args.limit,
                        tanks_arg=args.tanks,
                        dry_run=args.dry_run)
    print("Rows:", len(out))
    if not out.empty:
        print(out.head())

if __name__ == "__main__":
    main()



