# pipeline/train.py
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.utils import estimator_checks
from sklearn.utils._mask import _get_mask
from sklearn.compose import make_column_selector as selector
from .utils_sql import load_table, write_table
from .features import make_time_features   # thin wrapper around your _make_time_features
from .model_utils import fit_lgbm_dynamic, save_metrics, save_artifact_atomic
from pathlib import Path
import yaml, os, math
from .feature_groups import build_groups_dict
from .utils_sql import load_by_tanks   # in addition to load_table/write_table










def drop_by_groups(df, groups_to_drop=("weather","leakage"), extra_cols=(), keep=("tank_id", "updated_at", "median_level")):
    groups = build_groups_dict(df)
    to_drop = set()
    for g in groups_to_drop:
        to_drop.update([c for c in groups.get(g, []) if c in df.columns])
    to_drop.update([c for c in extra_cols if c in df.columns])
    # never drop essential keys
    to_drop = [c for c in to_drop if c not in keep]
    return df.drop(columns=to_drop, errors="ignore"), sorted(to_drop)


def log1p_clip(y): return np.log1p(np.maximum(y, 0))

def expm1_safe(y): return np.expm1(y)

def build_preprocess(X: pd.DataFrame):
    numeric_tf = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    categorical_tf = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('ohe', OneHotEncoder(handle_unknown='ignore'))
    ])
    return ColumnTransformer(
        transformers=[
            ('num', numeric_tf, selector(dtype_include=np.number)),
            ('cat', categorical_tf, selector(dtype_exclude=np.number))
        ],
        remainder='drop'
    )

def time_split(df, ts_col, cutoff_frac=0.8, cutoff_date=None):
    df = df.sort_values(ts_col)
    if cutoff_date is None:
        cut_idx = int(len(df) * cutoff_frac)
        cut_val = df[ts_col].iloc[cut_idx]
    else:
        cut_val = pd.to_datetime(cutoff_date)
    return df[df[ts_col] <= cut_val], df[df[ts_col] > cut_val], cut_val

def train_one(df, cfg, model_name, log_target=None):
    ts_col  = cfg['general']['ts_col']
    target  = cfg['general']['target']
    group   = cfg['general']['group_col']

    # let YAML decide unless explicitly overridden
    if log_target is None:
        log_target = bool(cfg['general'].get('log_target', True))

    # 1) drop groups/cols from config (after features, before split)
    gdrop = cfg.get('feature_drop', {}).get('groups', ["weather","leakage"])
    cdrop = cfg.get('feature_drop', {}).get('cols', [])
    df, dropped_cols = drop_by_groups(
        df,
        groups_to_drop=gdrop,
        extra_cols=cdrop,
        keep=(group, ts_col, target)
    
    )

    # 2) time-based split
    tr_df, te_df, cut = time_split(df, ts_col)
    if tr_df.empty or te_df.empty:
        raise ValueError("Train/test split is empty — adjust cutoff or data range.")

    y_tr, y_te = tr_df[target], te_df[target]
    X_tr = tr_df.drop(columns=[target])
    X_te = te_df.drop(columns=[target])

    # 3) preprocess
    prep = build_preprocess(X_tr)
    if log_target:
        ytr_fit = log1p_clip(y_tr.values.reshape(-1,1)).ravel()
        yte_fit = log1p_clip(y_te.values.reshape(-1,1)).ravel()
    else:
        ytr_fit, yte_fit = y_tr.values, y_te.values

    prep_fitted = prep.fit(X_tr, ytr_fit)
    Xtr = prep_fitted.transform(X_tr)
    Xva = prep_fitted.transform(X_te)

    # 4) train LGBM with dynamic trees (YAML params)
    lgb_cfg = cfg['lightgbm']
    model, best_iter, best_score, n_cap = fit_lgbm_dynamic(
        Xtr, ytr_fit, Xva, yte_fit,
        start_n=lgb_cfg['start_n'],
        max_n=lgb_cfg['max_n'],
        step_n=lgb_cfg['step_n'],
        learning_rate=lgb_cfg['learning_rate'],
        num_leaves=lgb_cfg['num_leaves'],
        stopping_rounds=lgb_cfg['stopping_rounds'],
        force_col_wise=bool(lgb_cfg.get('force_col_wise', True))  
    )

    # 5) predict + metrics
    import numpy as np, math
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

    y_pred = model.predict(Xva)
    if log_target:
        y_pred = np.expm1(y_pred)

    mae  = mean_absolute_error(y_te, y_pred)
    rmse = math.sqrt(mean_squared_error(y_te, y_pred))
    r2   = r2_score(y_te, y_pred)
    smape = 100.0 * np.mean(2*np.abs(y_pred - y_te) / (np.abs(y_te)+np.abs(y_pred)+1e-9))

    metrics = dict(MAE=mae, RMSE=rmse, R2=r2, sMAPE=smape,
                   best_iter=int(best_iter), n_cap=int(n_cap),
                   dropped=",".join(dropped_cols))

    # 6) return exactly THREE things (matches: art, m, cut)
    artifact = {"prep": prep_fitted, "model": model, "features": list(X_tr.columns)}
    return artifact, metrics, cut

   



def run_training(db_engine, cfg_path="config/tanks.yaml"):


    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)

    # 👇 add this debug here
    print(type(cfg), cfg.keys())
    print("general type:", type(cfg['general']), cfg['general'])

    base   = cfg['tables']['base']
    schema = cfg['tables'].get('schema')
    ts_col = cfg['general']['ts_col']
    target = cfg['general']['target']
    group  = cfg['general']['group_col']

    registry = cfg['paths']['registry']
    Path(registry).mkdir(parents=True, exist_ok=True)

    # ---- Cluster 0 ----
    g0 = cfg['groups']['cluster0']
    df_g0 = load_by_tanks(db_engine, base, g0, schema=schema, ts_col=ts_col)
    if not df_g0.empty:
        df_g0[ts_col] = pd.to_datetime(df_g0[ts_col], errors="coerce")
        df_g0 = df_g0.dropna(subset=[ts_col])
        df_g0_feat = make_time_features(df_g0, target=target, group_cols=[group], ts_col=ts_col)
        art, m, cut = train_one(df_g0_feat, cfg, "cluster0")  # train_one handles drop_by_groups
        path = save_artifact_atomic(art, registry, "cluster0") 
        save_metrics(m | {"model_name": "cluster0", "cutoff": str(cut)}, path)

    # ---- Individual tanks ----
    for tid in cfg['groups']['individual']:
        dft = load_by_tanks(db_engine, base, [tid], schema=schema, ts_col=ts_col)
        if dft.empty or len(dft) < 100:
            continue
        dft[ts_col] = pd.to_datetime(dft[ts_col], errors="coerce")
        dft = dft.dropna(subset=[ts_col])
        dft = make_time_features(dft, target=target, group_cols=[group], ts_col=ts_col)
        art, m, cut = train_one(dft, cfg, f"tank_{tid}")
        p = save_artifact_atomic(art, registry, f"tank_{tid}")    
        save_metrics(m | {"model_name": f"tank_{tid}", "cutoff": str(cut), "tank_id": tid}, p)

    # ---- Complex tanks ----
    for tid in cfg['groups']['complex']:
        dft = load_by_tanks(db_engine, base, [tid], schema=schema, ts_col=ts_col)
        if dft.empty or len(dft) < 100:
            continue
        dft[ts_col] = pd.to_datetime(dft[ts_col], errors="coerce")
        dft = dft.dropna(subset=[ts_col])
        dft = make_time_features(dft, target=target, group_cols=[group], ts_col=ts_col)
        art, m, cut = train_one(dft, cfg, f"tank_{tid}")
        p = save_artifact_atomic(art, registry, f"tank_{tid}")
        save_metrics(m | {"model_name": f"tank_{tid}", "cutoff": str(cut), "tank_id": tid}, p)


    # (Optionally) upsert all metrics into cfg['tables']['results'] here.
