# Liquido_data_analytics

**Liquidh₂O – Phase 1 : Data Analytics & Baseline Modeling**

**Goal**: Explore the predictive structure of water-level data and build an initial machine-learning baseline to test feasibility before time-aware modeling.

**Overview**

- Data: 13 tanks supplied exclusively by the main distribution network (no wells or alternative sources).

- Cadence: 30-minute readings of median_level, plus calendar, geographic, and weather variables.

- Approach: Exploratory modeling using PyCaret Regression to identify signal strength and relevant features.

-Algorithm: Extra Trees Regressor selected as best baseline.

- Split: Random 80 / 20 (train / validation).

**Key Findings**

- Strong, consistent predictive signal across tanks → confirms the viability of level forecasting.

- Most influential features: tank capacity and time-of-day / day-of-week indicators.

- Low-impact features: weather & geographic variables showed minimal correlation with water levels.

- Model performance: R² ≈ 0.99 (in-sample), MAE ≈ 1.3 — high accuracy but slight overfitting due to non-temporal split.

- Residuals: small and centered, indicating stable predictions even after removing tank IDs and coordinates.

**Results**
Metric	Score
R²	0.99
MAE	1.3
RMSE	2.4 (approx.)

**Interpretation**: The baseline model captures nearly all variation in tank levels but needs time-based validation to ensure generalization.

**Conclusions**

Phase 1 validated that water-level behavior is highly predictable and mainly governed by distribution schedules rather than environmental factors.
These insights established the foundation for a production-ready, time-aware pipeline.

**Next Steps → Phase 2**

- Introduce chronological train/test splits to simulate real forecasting.

- Add lag, rolling, and seasonal features for temporal awareness.

- Re-implement with Extra Trees / LightGBM for scalable modeling.

- Build per-tank performance tracking and anomaly-detection logic.

