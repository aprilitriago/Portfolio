# pipeline/model_utils.py
from pathlib import Path
import json, joblib, shutil
from datetime import datetime, timezone
import lightgbm as lgb
from lightgbm import early_stopping, log_evaluation


# ---------- helpers ----------
def _timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%S")

def _is_new_style_dir(p: Path) -> bool:
    return (p / "model.pkl").exists() and (p / "prep.pkl").exists()

def _is_old_style_dir(p: Path) -> bool:
    return (p / "model.joblib").exists()

# ---------- discover latest ----------
def latest_artifact_path(registry: str, model_name: str):
    root = Path(registry) / model_name
    if not root.exists():
        return None
    candidates = [
        p for p in root.iterdir()
        if p.is_dir() and (_is_new_style_dir(p) or _is_old_style_dir(p))
    ]
    return max(candidates, key=lambda p: p.stat().st_mtime) if candidates else None

# ---------- atomic save ----------
def save_artifact_atomic(artifact: dict, registry: str, model_name: str) -> str:
    """
    Atomically write artifacts to {registry}/{model_name}/{timestamp}/
    Files: model.pkl, prep.pkl, features.json
    """
    root = Path(registry) / model_name
    run_dir = root / _timestamp()
    tmp_dir = run_dir.with_name(run_dir.name + "_tmp")

    tmp_dir.mkdir(parents=True, exist_ok=True)
    joblib.dump(artifact["model"], tmp_dir / "model.pkl")
    joblib.dump(artifact["prep"],  tmp_dir / "prep.pkl")
    with open(tmp_dir / "features.json", "w", encoding="utf-8") as f:
        json.dump({"features": artifact.get("features", [])}, f)

    if run_dir.exists():
        shutil.rmtree(run_dir)
    tmp_dir.rename(run_dir)  # promote tmp -> final atomically
    return str(run_dir)

# ---------- save metrics ----------
def save_metrics(metrics: dict, artifact_dir: str | Path) -> None:
    artifact_dir = Path(artifact_dir)
    artifact_dir.mkdir(parents=True, exist_ok=True)
    with open(artifact_dir / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, ensure_ascii=False, indent=2)

# ---------- load (new or legacy) ----------
def load_artifact(registry: str, model_name: str):
    """
    Loads latest artifact folder (supports new model.pkl/prep.pkl and legacy model.joblib).
    Returns {"model": ..., "prep": ..., "features": [...], "path": Path} or None.
    """
    p = latest_artifact_path(registry, model_name)
    if p is None:
        return None

    # New layout
    if _is_new_style_dir(p):
        model = joblib.load(p / "model.pkl")
        prep  = joblib.load(p / "prep.pkl")
        feats = []
        fp = p / "features.json"
        if fp.exists():
            try:
                with open(fp, "r", encoding="utf-8") as f:
                    feats = json.load(f).get("features", [])
            except Exception:
                feats = []
        return {"model": model, "prep": prep, "features": feats, "path": p}

    # Legacy layout
    if _is_old_style_dir(p):
        blob = joblib.load(p / "model.joblib")
        if isinstance(blob, dict) and "model" in blob:
            return {"model": blob["model"], "prep": blob.get("prep"),
                    "features": blob.get("features", []), "path": p}
        return {"model": blob, "prep": None, "features": [], "path": p}

    return None

# --- LightGBM dynamic trainer ---

def fit_lgbm_dynamic(
    Xtr, ytr, Xva, yva,
    start_n=3000, max_n=7000, step_n=1000,
    learning_rate=0.05, num_leaves=64,
    subsample=0.8, colsample_bytree=0.8,
    random_state=42, stopping_rounds=80,
    force_col_wise=True  # helps with memory
):
    callbacks = [early_stopping(stopping_rounds, verbose=False), log_evaluation(0)]
    n = start_n
    best = None
    while True:
        model = lgb.LGBMRegressor(
            n_estimators=n,
            learning_rate=learning_rate,
            num_leaves=num_leaves,
            subsample=subsample,
            colsample_bytree=colsample_bytree,
            n_jobs=-1,
            random_state=random_state,
            force_col_wise=force_col_wise
        )
        model.fit(Xtr, ytr, eval_set=[(Xva, yva)], callbacks=callbacks)
        bi = getattr(model, "best_iteration_", n)
        score = getattr(model, "best_score_", {})
        best = (model, bi, score, n)
        if bi < n or n >= max_n:
            break
        n = min(n + step_n, max_n)
    return best  # (model, best_iter, best_score, n_cap)
