# cli.py
import argparse, yaml
from pipeline.utils_sql import get_engine

from pipeline.predict import predict_batch
from pipeline.monitor import compute_recent_metrics
import pandas as pd

def cmd_train(args):
    from pipeline.train import run_training
    eng = get_engine()
    run_training(eng, cfg_path=args.cfg)

def cmd_predict(args):
    eng = get_engine()
    out = predict_batch(
        eng,
        cfg_path=args.cfg,
        limit=args.limit,
        tanks_arg=args.tanks,
        dry_run=args.dry_run,
        model_ver=args.model_ver,
    )
    print("Rows:", len(out))
    if not out.empty:
        print(out.head())

def cmd_monitor(args):
    eng = get_engine()

    preds_table = args.preds_table
    truth_table = args.truth_table
    ts_col = args.ts_col
    target = args.target
    group = args.group

    # If a YAML config is provided, prefer it
    if args.cfg:
        with open(args.cfg, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        tcfg = cfg.get("tables", {})
        preds_table_yaml = tcfg.get("preds")
        preds_schema_yaml = tcfg.get("schema")
        truth_table_yaml = tcfg.get("base")
        truth_schema_yaml = tcfg.get("base_schema")

        if preds_table_yaml:
            preds_table = (
                f"{preds_schema_yaml}.{preds_table_yaml}"
                if preds_schema_yaml
                else preds_table_yaml
            )
        if truth_table_yaml:
            truth_table = (
                f"{truth_schema_yaml}.{truth_table_yaml}"
                if truth_schema_yaml
                else truth_table_yaml
            )

        gcfg = cfg.get("general", {})
        ts_col = gcfg.get("ts_col", ts_col)
        target = gcfg.get("target", target)
        group = gcfg.get("group_col", group)

    if args.preds_schema:
        preds_table = f"{args.preds_schema}.{preds_table}"
    if args.truth_schema:
        truth_table = f"{args.truth_schema}.{truth_table}"

    df = compute_recent_metrics(
        db_engine=eng,
        preds_table=preds_table,
        truth_table=truth_table,
        horizon_days=args.horizon_days,
        ts_col=ts_col,
        target=target,
        group=group,
    )
    if df.empty:
        print("No recent metrics computed (empty join).")
    else:
        print(df.head().to_string(index=False))

def main():
    ap = argparse.ArgumentParser(prog="pipeline-cli")
    sub = ap.add_subparsers(dest="cmd", required=True)

    ap_tr = sub.add_parser("train", help="Run training with a YAML config")
    ap_tr.add_argument("--cfg", required=True, help="Path to tanks_train.yaml")
    ap_tr.set_defaults(func=cmd_train)

    ap_pr = sub.add_parser("predict", help="Run batch prediction with a YAML config")
    ap_pr.add_argument("--cfg", required=True, help="Path to tanks_predict.yaml")
    ap_pr.add_argument("--limit", type=int, default=None)
    ap_pr.add_argument("--tanks", type=str, default=None)
    ap_pr.add_argument("--dry-run", action="store_true")
    ap_pr.add_argument("--model-ver", type=str, default="lgbm_v1")
    ap_pr.set_defaults(func=cmd_predict)

    ap_mo = sub.add_parser("monitor", help="Compute recent metrics from DB tables")
    ap_mo.add_argument("--cfg", help="Path to tanks_predict.yaml (optional)")
    ap_mo.add_argument("--preds-table", help="Predictions table (optional)")
    ap_mo.add_argument("--truth-table", help="Truth table (optional)")
    ap_mo.add_argument("--preds-schema", help="Schema for predictions table (optional)")
    ap_mo.add_argument("--truth-schema", help="Schema for truth table (optional)")
    ap_mo.add_argument("--horizon-days", type=int, default=14)
    ap_mo.add_argument("--ts-col", default="updated_at")
    ap_mo.add_argument("--target", default="median_level")
    ap_mo.add_argument("--group", default="tank_id")
    ap_mo.set_defaults(func=cmd_monitor)

    args = ap.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
