# pipeline/monitor.py
import pandas as pd
import numpy as np
from .utils_sql import load_table, write_table

def compute_recent_metrics(db_engine, preds_table, truth_table, horizon_days=14,
                           ts_col="updated_at", target="median_level", group="tank_id"):
    # join last N days predictions with truth, compute MAE/RMSE/R2/sMAPE per tank
    preds = load_table(db_engine, preds_table)
    truth = load_table(db_engine, truth_table)
    preds[ts_col] = pd.to_datetime(preds[ts_col])
    truth[ts_col] = pd.to_datetime(truth[ts_col])
    cutoff = preds[ts_col].max() - pd.Timedelta(days=horizon_days)

    m = (preds[preds[ts_col] >= cutoff]
         .merge(truth[[group, ts_col, target]], on=[group, ts_col], how="inner"))
    if m.empty: return pd.DataFrame()

    y, yhat = m[target].values, m["median_level_pred"].values
    def smape(a, b): return 100*np.mean(2*np.abs(a-b)/(np.abs(a)+np.abs(b)+1e-9))
    out = (m.groupby(group)
           .apply(lambda g: pd.Series({
               "MAE": np.mean(np.abs(g[target]-g["median_level_pred"])),
               "RMSE": np.sqrt(np.mean((g[target]-g["median_level_pred"])**2)),
               "R2": 1 - np.sum((g[target]-g["median_level_pred"])**2)/np.sum((g[target]-g[target].mean())**2 + 1e-9),
               "sMAPE": smape(g[target], g["median_level_pred"])
           }))
           .reset_index())
    return out
