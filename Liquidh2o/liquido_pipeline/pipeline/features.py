# pipeline/features.py
import pandas as pd

def make_time_features(
    df: pd.DataFrame,
    target: str,
    group_cols=("tank_id",),
    ts_col="updated_at",
    lags=(1,2,3,6,12),
    roll_windows=(3,6,12,24),
    seasonal_lags=(48,96,336),
):
    df = df.copy()
    df[ts_col] = pd.to_datetime(df[ts_col], errors="coerce")
    df = df.dropna(subset=[ts_col]).sort_values(list(group_cols)+[ts_col])

    # simple lags
    for L in lags:
        df[f"{target}_lag{L}"] = df.groupby(list(group_cols))[target].shift(L)

    # rolling stats (shift to avoid leakage)
    for W in roll_windows:
        s = df.groupby(list(group_cols))[target].shift(1)
        df[f"{target}_rollmean{W}"] = s.rolling(W, min_periods=max(1,int(0.7*W))).mean()
        df[f"{target}_rollstd{W}"]  = s.rolling(W, min_periods=max(1,int(0.7*W))).std()

    # seasonal lags (e.g., 48 for 1 day @ 30-min freq)
    for S in seasonal_lags:
        df[f"{target}_seaslag{S}"] = df.groupby(list(group_cols))[target].shift(S)

    # calendar
    df["hour"]  = df[ts_col].dt.hour
    df["dow"]   = df[ts_col].dt.dayofweek
    df["month"] = df[ts_col].dt.month
    return df
