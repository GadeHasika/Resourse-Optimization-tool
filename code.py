import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import pmdarima as pm
import psutil
import time
import os
import warnings
warnings.filterwarnings("ignore")
 
DATA_FILE = "cpu_data.csv"
FORECAST_HOURS = 24
cost_per_server = 500  
exchange_rate = 83  
 
def collect_live_data(duration_minutes=2, interval_seconds=5):
    data = []
    start_time = pd.Timestamp.now()
    with st.spinner(f"Collecting live data for {duration_minutes} minutes..."):
        while (pd.Timestamp.now() - start_time).seconds < duration_minutes * 60:
            cpu = psutil.cpu_percent(interval=1)
            mem = psutil.virtual_memory().percent
            data.append([pd.Timestamp.now(), cpu, mem])
            time.sleep(max(0, interval_seconds - 1))
    return pd.DataFrame(data, columns=['date', 'cpu_usage', 'memory_usage'])

def save_samples(df, filename=DATA_FILE):
    if os.path.exists(filename):
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        df.to_csv(filename, index=False)

def load_data(filename=DATA_FILE):
    if os.path.exists(filename):
        df = pd.read_csv(filename, parse_dates=['date'])
        df = df.drop_duplicates(subset=['date']).sort_values('date')
        df = df.set_index('date')
        df = df.resample('5min').mean().ffill()
        return df
    else:
        return pd.DataFrame()

def forecast_series(series, hours=24):
    """Forecasts using ARIMA or repeats last value if insufficient data."""
    if len(series) < 10:
        return pd.Series([series.iloc[-1]] * hours,
                         index=pd.date_range(series.index[-1] + pd.Timedelta(hours=1), periods=hours, freq='h'))
    try:
        model = pm.auto_arima(series, seasonal=False, suppress_warnings=True, error_action='ignore', max_p=3, max_q=3, max_order=5)
        fc = model.predict(n_periods=hours)
        future = pd.date_range(start=series.index[-1] + pd.Timedelta(hours=1), periods=hours, freq='h')
        return pd.Series(fc, index=future)
    except:
        return pd.Series([series.iloc[-1]] * hours,
                         index=pd.date_range(series.index[-1] + pd.Timedelta(hours=1), periods=hours, freq='h'))

def scaling_recommendation(peak_cpu, peak_mem, threshold_cpu, threshold_mem):
    """Recommends scaling based on whichever (CPU or Memory) is higher relative to its threshold."""
    recs = [] 
    if peak_cpu > threshold_cpu:
        needed = int(np.ceil((peak_cpu - threshold_cpu) / 10))
        cost_usd = needed * cost_per_server
        cost_inr = cost_usd * exchange_rate
        recs.append(f"CPU: Scale UP by {needed} server(s). Cost ≈ ${cost_usd} (~₹{cost_inr:,.0f}).")
    elif peak_cpu < threshold_cpu - 20:
        remove = int(np.floor((threshold_cpu - peak_cpu) / 10))
        saving_usd = remove * cost_per_server
        saving_inr = saving_usd * exchange_rate
        recs.append(f"CPU: Scale DOWN by {remove} server(s). Saving ≈ ${saving_usd} (~₹{saving_inr:,.0f}).")
    else:
        recs.append("CPU: No scaling needed.") 
    if peak_mem > threshold_mem:
        needed = int(np.ceil((peak_mem - threshold_mem) / 10))
        cost_usd = needed * cost_per_server
        cost_inr = cost_usd * exchange_rate
        recs.append(f"Memory: Scale UP by {needed} server(s). Cost ≈ ${cost_usd} (~₹{cost_inr:,.0f}).")
    elif peak_mem < threshold_mem - 20:
        remove = int(np.floor((threshold_mem - peak_mem) / 10))
        saving_usd = remove * cost_per_server
        saving_inr = saving_usd * exchange_rate
        recs.append(f"Memory: Scale DOWN by {remove} server(s). Saving ≈ ${saving_usd} (~₹{saving_inr:,.0f}).")
    else:
        recs.append("Memory: No scaling needed.")
    return recs 
st.title("CPU & Memory Usage Forecast & Scaling Recommendation")
st.markdown("Monitor **CPU** & **Memory** usage, forecast future needs, and get scaling recommendations with cost in **INR**.")
 
st.sidebar.header("⚙️ Settings")
THRESHOLD_CPU = st.sidebar.slider("CPU Threshold (%)", min_value=50, max_value=95, value=80, step=1)
THRESHOLD_MEM = st.sidebar.slider("Memory Threshold (%)", min_value=50, max_value=95, value=75, step=1)
INTERVAL_SECONDS = st.sidebar.number_input("Data Collection Interval (seconds)", min_value=1, max_value=60, value=5)
DURATION_MINUTES = st.sidebar.number_input("Data Collection Duration (minutes)", min_value=1, max_value=10, value=2)

# Collect live data button
if st.button("Collect Live Data"):
    df_new = collect_live_data(DURATION_MINUTES, INTERVAL_SECONDS)
    save_samples(df_new)
    st.success(f"New live data collected and saved! ({len(df_new)} samples)")

df_all = load_data()

if df_all.empty:
    st.warning("No data available. Please collect live data first.")
else:
    # Forecast CPU & Memory
    forecasted_cpu = forecast_series(df_all['cpu_usage'], hours=FORECAST_HOURS)
    forecasted_mem = forecast_series(df_all['memory_usage'], hours=FORECAST_HOURS)

    # ───── Separate CPU Graph ─────
    st.subheader("CPU Usage (Historical)")
    fig_cpu = go.Figure()
    fig_cpu.add_trace(go.Scatter(
        x=df_all.index, y=df_all['cpu_usage'],
        mode='lines+markers',
        name='CPU Usage',
        hovertemplate='Time: %{x}<br>CPU: %{y:.1f}%',
        line=dict(color='blue')
    ))
    fig_cpu.add_hline(
        y=THRESHOLD_CPU,
        line=dict(color='red', dash='dot'),
        annotation_text=f"CPU Threshold {THRESHOLD_CPU}%",
        annotation_position="top right"
    )
    fig_cpu.update_layout(
        title="CPU Usage Trends",
        xaxis_title="Time",
        yaxis_title="CPU Usage (%)",
        template="plotly_white",
        hovermode="x unified"
    )
    st.plotly_chart(fig_cpu, use_container_width=True)


    st.subheader("Memory Usage (Historical)")
    fig_mem = go.Figure()
    fig_mem.add_trace(go.Scatter(
        x=df_all.index, y=df_all['memory_usage'],
        mode='lines+markers',
        name='Memory Usage',
        hovertemplate='Time: %{x}<br>Memory: %{y:.1f}%',
        line=dict(color='green')
    ))
    fig_mem.add_hline(
        y=THRESHOLD_MEM,
        line=dict(color='orange', dash='dot'),
        annotation_text=f"Memory Threshold {THRESHOLD_MEM}%",
        annotation_position="top right"
    )
    fig_mem.update_layout(
        title="Memory Usage Trends",
        xaxis_title="Time",
        yaxis_title="Memory Usage (%)",
        template="plotly_white",
        hovermode="x unified"
    )
    st.plotly_chart(fig_mem, use_container_width=True)

    peak_cpu = forecasted_cpu.max()
    peak_mem = forecasted_mem.max()
    st.subheader("Scaling Recommendations")
    st.metric(label="Predicted Peak CPU (Next 24h)", value=f"{peak_cpu:.1f}%")
    st.metric(label="Predicted Peak Memory (Next 24h)", value=f"{peak_mem:.1f}%")
    recs = scaling_recommendation(peak_cpu, peak_mem, THRESHOLD_CPU, THRESHOLD_MEM)
    for rec in recs:
        st.info(rec)




















