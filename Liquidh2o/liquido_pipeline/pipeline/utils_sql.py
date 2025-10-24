# pipeline/utils_sql.py
import os
import numpy as np
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from typing import Optional, Union, Sequence, Dict
from .clean import clean_target_per_tank



def get_engine() -> Engine:
    """Build engine using local .env or default connection values."""
    pg_user     = os.getenv("pg_user", "postgres")
    pg_password = os.getenv("pg_password", "3rb414350638")  
    pg_host     = os.getenv("pg_host", "localhost")
    pg_port     = os.getenv("pg_port", "5432")
    pg_dbname   = os.getenv("pg_dbname", "liquidosep")

    url = f"postgresql+psycopg2://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_dbname}"
    return create_engine(url)

def load_table(engine_or_url, table, schema: Optional[str]=None, where: Optional[str]=None):
    if isinstance(engine_or_url, Engine):
        eng = engine_or_url
    else:
        eng = create_engine(engine_or_url)

    fq = f"{schema}.{table}" if schema else table
    sql = f"SELECT * FROM {fq}" + (f" WHERE {where}" if where else "")
    return pd.read_sql(sql, eng)





def load_by_tanks(
    engine: Engine,
    table: str,
    tank_ids: Sequence[int],
    schema: Optional[str] = None,
    ts_col: Optional[str] = None,
    time_from: Optional[str] = None,   # e.g., "2024-01-01"
    time_to: Optional[str] = None      # e.g., "2025-10-01"
) -> pd.DataFrame:
    """
    Load rows for a set of tank_ids from schema.table with optional time range.
    Uses bound parameters to avoid SQL injection.
    """
    if not tank_ids:
        return pd.DataFrame()

    fq = f"{schema}.{table}" if schema else table

    # Build a safe IN (...) with named params :id0, :id1, ...
    placeholders = ", ".join([f":id{i}" for i in range(len(tank_ids))])
    where = [f"tank_id IN ({placeholders})"]

    params: Dict[str, object] = {f"id{i}": tid for i, tid in enumerate(tank_ids)}

    if ts_col and time_from:
        where.append(f"{ts_col} >= :time_from")
        params["time_from"] = time_from
    if ts_col and time_to:
        where.append(f"{ts_col} < :time_to")
        params["time_to"] = time_to

    sql = text(f"SELECT * FROM {fq} WHERE " + " AND ".join(where))
    df = pd.read_sql(sql, engine, params=params)
    if ts_col in df.columns:
        df[ts_col] = pd.to_datetime(df[ts_col], errors="coerce")
    return df


def write_table(
    df: pd.DataFrame,
    engine_or_url: Union[str, Engine],
    table: str,
    schema: Optional[str] = None,
    if_exists: str = "replace"
) -> None:
    """Write a DataFrame to SQL (create or replace table)."""
    if isinstance(engine_or_url, Engine):
        eng = engine_or_url
    else:
        eng = create_engine(engine_or_url)

    df.to_sql(
        table,
        eng,
        schema=schema,
        if_exists=if_exists,
        index=False
    )

def clean_target_per_tank(df, target="median_level", cap_quantile=0.995):
    df = df.copy()
    caps = df.groupby("tank_id")[target].quantile(cap_quantile).rename("cap")
    df = df.merge(caps, on="tank_id", how="left")

    # new column only for analysis
    df["median_level_capped"] = np.minimum(df[target], df["cap"])
    df = df.drop(columns=["cap"])
    return df    