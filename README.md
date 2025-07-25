🚀 Overview
Managing IT resources efficiently is a critical challenge for organizations.
Over-provisioning leads to wasted costs, while under-provisioning can cause downtime and performance issues.

This project delivers an AI-driven web application that helps:

Monitor real-time CPU & memory usage

Forecast future demand (24h) using ARIMA

Recommend scaling actions (add/remove servers)

Provide cost insights in USD & INR

✨ Key Features
1. Real-Time Monitoring

Live collection of CPU & memory usage with customizable intervals.

Stores data in cpu_data.csv for historical analysis.

2. Interactive Visualizations
Two separate Plotly charts:

CPU Usage (with thresholds)

Memory Usage (with thresholds)

Aggregated to 1-minute intervals for better readability.

3. AI-Powered Forecasting
pmdarima.auto_arima automatically selects the best ARIMA model.

Forecasts CPU & memory usage for the next 24 hours.

4. Smart Scaling Recommendations
Compares predicted peaks with user-defined thresholds.

Suggests Scale Up/Down actions.

Estimates costs & savings in USD & INR.

🛠️ Tech Stack
Python: pandas, numpy, psutil, pmdarima, plotly

Streamlit: For the interactive dashboard

ARIMA: For time-series forecasting

CSV: For persistent data storage

📂 How It Works

Live Data Collection

Captures CPU & memory usage periodically using psutil.

Data Storage

Saves readings into cpu_data.csv.

Forecasting

Uses ARIMA to forecast demand for next 24 hours.

Scaling Decision

Compares predicted peaks with thresholds.

Calculates servers to add/remove.

Shows cost impact in USD & INR.

