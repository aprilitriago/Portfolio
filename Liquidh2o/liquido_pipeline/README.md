# Liquidh2o – Water Tank Analytics & Forecasting

Time-aware LightGBM to predict tank levels. Reads from PostgreSQL views, builds lag/rolling/seasonal features, saves per-tank artifacts, and upserts predictions.

## Configs (your exact setup)

- **Training** → `config/tanks_train.yaml`
  - read from: `public.view_measurements_ml` → (you clean into) `pipeline.view_measurements_ml_clean`
  - write to: `pipeline.ml_results`, `pipeline.tank_predictions`
  - artifacts: `models/`
- **Predict** → `config/tanks_predict.yaml`
  - read from: `predictions.view_measurements_predict_8d` (past+future window)
  - write to: `predictions.future_levels`
  - artifacts: `models/`

## Quickstart

```bash
# 0) Env + install
cp .env.example .env
python -m venv .venv && source .venv/bin/activate   # (Win: .venv\Scripts\activate)
pip install -r requirements.txt
pip install -e .

# 1) Train (uses your run_training)
python - <<'PY'
from pipeline.train import run_training
from pipeline.utils_sql import get_engine
run_training(get_engine(), "config/tanks_train.yaml")
PY

# 2) Predict (entrypoint in monitor.py)
python -m pipeline.monitor --cfg config/tanks_predict.yaml --model-ver lgbm_v1
# extras: --dry-run, --limit 10, --tanks "31,69"


.
├─ pipeline/
│  ├─ train.py, monitor.py, features.py, feature_groups.py, model_utils.py, clean.py, utils_sql.py
├─ config/
│  ├─ tanks_train.yaml
│  └─ tanks_predict.yaml
├─ models/  artifacts/
├─ .env.example  requirements.txt  Dockerfile  setup.py  README.md  runbook.md
