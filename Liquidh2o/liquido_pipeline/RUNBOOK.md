# Runbook

## 0) Preconditions
- DB has:
  - `public.view_measurements_ml` (raw)
  - `pipeline.view_measurements_ml_clean` (cleaned, used for training)
  - `predictions.view_measurements_predict_8d` (past+future window for inference)
- Copy `.env.example` → `.env` (lowercase keys match `utils_sql.get_engine`).

## 1) Install
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -e .

2) Train

Config: config/tanks_train.yaml

Reads: public.view_measurements_ml (then you persist/consume the cleaned pipeline.view_measurements_ml_clean)
Writes: artifacts under models/, metrics JSON per run.
Tank groups: cluster0, individual, complex (as listed).
Feature drop: groups ["weather","leakage"], cols ["median_level_capped"].

python - <<'PY'
from pipeline.train import run_training
from pipeline.utils_sql import get_engine
run_training(get_engine(), "config/tanks_train.yaml")
PY



