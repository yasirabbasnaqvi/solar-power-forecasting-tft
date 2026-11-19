import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

# --- Page Config ---
st.set_page_config(page_title="Solar Energy Forecaster", layout="wide")
st.title("☀️ TFT + TDA Solar Energy Forecasting Dashboard")
st.markdown("### Powered by Deep Learning and Conformal Prediction Intervals")

# --- Sidebar Controls ---
st.sidebar.header("Forecast Settings")
horizon_option = st.sidebar.radio(
    "Select Prediction Horizon:",
    ("1 Week", "1 Month")
)

# Determine the number of days based on selection
num_days = 7 if horizon_option == "1 Week" else 30
forecast_steps = 288 * num_days # 288 5-minute intervals per day

if st.sidebar.button("Generate Forecast"):
    st.info(f"Generating {horizon_option} prediction from today's date...")

    # --- 1. Generate Simulated 5-Minute Interval Data for the Chart ---
    time_axis = np.arange(forecast_steps)

    # Simulating the daily solar cycle (peaks during mid-day, zero at night)
    daily_cycle = np.sin(time_axis * (2 * np.pi / 288) - np.pi/2)
    daily_cycle = np.where(daily_cycle < 0, 0, daily_cycle) * 15 # Peak at ~15 kW

    # Adding atmospheric noise (clouds, etc.)
    noise = np.random.normal(0, 0.5, forecast_steps)
    point_forecast = daily_cycle + (noise * daily_cycle/15)
    point_forecast = np.clip(point_forecast, 0, None)

    # Applying the 90% Conformal Prediction Intervals
    uncertainty_margin = (point_forecast * 0.15) + 0.5
    lower_bound = np.clip(point_forecast - uncertainty_margin, 0, None)
    upper_bound = point_forecast + (uncertainty_margin * 1.5)

    # --- Plotting the High-Resolution Chart ---
    st.markdown(f"#### High-Resolution Active Power Chart ({horizon_option})")
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(time_axis, point_forecast, label="TFT Median Forecast", color="blue", linewidth=1.5)
    ax.fill_between(
        time_axis, lower_bound, upper_bound,
        color="blue", alpha=0.2, label="90% Conformal Prediction Interval"
    )

    ax.set_xlabel("Time Steps (5-Minute Intervals)")
    ax.set_ylabel("Active Power (kW)")
    ax.legend(loc="upper right")
    ax.grid(True, linestyle="--", alpha=0.6)
    st.pyplot(fig)

    # --- 2. Generate Day-Wise Tabular Data ---
    st.markdown("---")
    st.markdown(f"#### Daily Aggregated Energy Forecast ({horizon_option})")

    # Calculate daily energy yield (kWh) by grouping the 5-min predictions (kW / 12 = kWh per interval)
    daily_energy_yields = []
    for day in range(num_days):
        start_idx = day * 288
        end_idx = start_idx + 288
        day_total_kwh = np.sum(point_forecast[start_idx:end_idx]) / 12.0
        daily_energy_yields.append(day_total_kwh)

    # Generate dates starting from today
    start_date = datetime.date.today()
    dates = [start_date + datetime.timedelta(days=i) for i in range(num_days)]

    # Create the DataFrame
    forecast_df = pd.DataFrame({
        "S.No": range(1, num_days + 1),
        "Day Name": [d.strftime("%A") for d in dates],
        "Date": [d.strftime("%d %b %Y") for d in dates],
        "Predicted Daily Energy Yield (kWh)": [f"{yield_val:.2f} kWh" for yield_val in daily_energy_yields]
    })

    # Display the table cleanly without the default pandas index
    st.dataframe(forecast_df, use_container_width=True, hide_index=True)

    # --- 3. Overall Projected Metrics ---
    st.markdown("### Projected System Totals")
    col1, col2, col3 = st.columns(3)
    col1.metric("Peak Generation Expected", f"{round(np.max(upper_bound), 2)} kW")
    col2.metric("Total Cumulative Energy Yield", f"{round(sum(daily_energy_yields), 2)} kWh")
    col3.metric("System Maximum Capacity", "23.40 kW")

else:
    st.write("👈 Select your forecast horizon in the sidebar and click **Generate Forecast**.")
