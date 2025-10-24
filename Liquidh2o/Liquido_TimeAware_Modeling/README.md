# Liquido_TimeAware_Modeling

**Liquidh₂O – Phase 2 : Time-Aware Forecasting**

**Goal**: Extend the Phase 1 baseline into a time-aware model that predicts short-term water-level changes for distribution-only tanks.

**Overview**

- Data: 13 tanks, 30-minute readings (median_level).
- Split: 80 % training (earliest dates), 20 % testing (future hold-out).
- Period: May 17 – June 12 2025.
- Algorithm: Extra Trees Regressor (600 trees, log-target).
- Metrics: MAE, RMSE, R², RMSLE, sMAPE.

**Key Improvements**

- Added lags (1–12), rolling stats (3–24), and seasonal lags (48, 96, 336) to capture temporal cycles.
- Dropped weather variables → no predictive power.
- Dropped slope_30 → target leakage.
- Used a chronological split for true forecasting evaluation.

**Results**
**Metric	Score**
- MAE	4.68
- RMSE	11.45
- R²	0.975
 - sMAPE	4.6 %

**Interpretation:** The model explains 97 % of water-level variance with average errors under 5 units.
**Next Steps**
- Transition to LightGBM for faster, scalable retraining.
- Automate SQL export and monitoring dashboards.
- Add anomaly-detection thresholds for real-time alerts.
