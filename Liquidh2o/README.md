# Liquidh2o
This project develops a predictive analytics and machine learning pipeline to monitor and control water distribution across client tanks. It uses time-series modeling to ensure that each tank’s predicted water level aligns with the measured level, allowing automatic control and early anomaly detection.

The analysis integrates sensor data from the distribution network with weather and temporal features, applying advanced preprocessing steps such as lag and rolling-window feature engineering, outlier handling, and winsorization to stabilize readings.

An Extra Trees baseline was first trained using PyCaret to validate signal strength, achieving an R² above 0.99 across most tanks. The next phase migrates to LightGBM for improved scalability and interpretability, with per-tank models deployed through automated Python–SQL pipelines for daily monitoring.
