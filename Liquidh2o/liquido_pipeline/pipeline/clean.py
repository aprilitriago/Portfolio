# pipeline/clean.py
import numpy as np
import pandas as pd


def clean_target_per_tank(df, target="median_level", cap_quantile=0.995):
    df = df.copy()
    caps = df.groupby("tank_id")[target].quantile(cap_quantile).rename("cap")
    df = df.merge(caps, on="tank_id", how="left")

    # new column only for analysis
    df["median_level_capped"] = np.minimum(df[target], df["cap"])
    df = df.drop(columns=["cap"])
    return df
