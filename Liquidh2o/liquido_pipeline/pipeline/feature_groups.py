# pipeline/feature_groups.py
import numpy as np

def build_groups_dict(df=None):
    groups = {
        "ids": ["tank_id","id"],
        "weather": [
            "temp","temperature","humidity","pressure","wind_speed","wind_dir",
            "rain","precipitation","dewpoint","cloud_cover","solar_radiation",
            "weather_temp","weather_humidity","weather_pressure","weather_wind_speed",
            "weather_rain","weather_precipitation","weather_clouds",
            "tank_temp","tank_precip","tank_humidity","dam_temp","dam_precip","dam_humidity"
        ],
        "leakage": ["leakage","leakage_flag","leak_flag","leak_prob","is_leak","slope_30"]
    }
    if df is not None:
        cols = list(df.columns)
        wx = [c for c in cols if c.startswith("weather_")]
        if wx: groups["weather"] = sorted(set(groups["weather"] + wx))
        leak = [c for c in cols if c.startswith("leak") or c.endswith("_leak")]
        if leak: groups["leakage"] = sorted(set(groups["leakage"] + leak))
    return groups
