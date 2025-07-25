Managing IT resources efficiently is a major challenge for organizations. Over-provisioning leads to wasted costs, while under-provisioning can cause downtime and performance degradation.
This project is an AI-driven dashboard that provides:

Real-time monitoring of CPU & memory usage
24-hour forecasting using ARIMA
Automated scaling recommendations (scale up/down)
Cost analysis in USD & INR
The solution empowers IT teams to make data-driven decisions for capacity planning and cost optimization.
Key Features
1. Real-Time Data Collection
Collects live CPU & memory usage using psutil.

Flexible collection interval & duration (set via the sidebar).

2. Historical Data Storage
Saves usage data to cpu_data.csv for long-term tracking.

3. Interactive Visualizations
Two separate Plotly charts:
CPU Usage (with thresholds)
Memory Usage (with thresholds)
Aggregated to 1-minute intervals for clean visualization.

4. AI-Powered Forecasting
Uses pmdarima.auto_arima to automatically select the best ARIMA model.
Predicts CPU & memory usage for the next 24 hours.

5. Intelligent Scaling Recommendations
Compares predicted peak usage with user-defined thresholds.

Recommends:
Scale Up (add servers if demand is high)
Scale Down (remove servers if under-utilized)
Estimates costs/savings in USD & INR.

Tech Stack
Python: pandas, numpy, psutil, pmdarima, plotly
Streamlit: Interactive web dashboard
ARIMA (pmdarima): For time-series forecasting
CSV Storage: Persistent data logging 
