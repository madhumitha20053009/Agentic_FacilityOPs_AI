
import sys
from pathlib import Path

import streamlit as st
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from agents.energy_agent import run_energy_agent
from database.db import save_energy_data

st.set_page_config(
    page_title="Agentic FacilityOps AI",
    layout="wide"
)

st.title("Agentic FacilityOps AI")
st.subheader("Smart Energy Monitoring and Anomaly Detection Dashboard")
st.divider()

# Run Energy Agent
result = run_energy_agent()
df = result["data"]

# Save data to SQLite
save_energy_data(df)

# Energy Overview
st.header("Energy Consumption Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Energy Usage", f"{df['energy_kwh'].sum():.2f} kWh")
col2.metric("Average Daily Usage", f"{result['average_usage']:.2f} kWh")
col3.metric("Detected Anomalies", len(result["anomalies"]))

st.divider()

# Daily Energy Chart
st.header("Daily Energy Consumption")

if not df.empty:
    st.line_chart(df.set_index("date")["energy_kwh"])
else:
    st.warning("No energy data available.")

st.divider()

# Energy Status Analysis
st.header("Energy Status Analysis")

anomaly_count = len(result["anomalies"])
normal_count = max(0, len(df) - anomaly_count)

status_count = pd.Series({
    "Normal": normal_count,
    "Anomaly": anomaly_count
})

st.bar_chart(status_count)

st.divider()

# Anomaly Alerts
st.header("Anomaly Detection Alerts")

if result["anomalies"]:
    st.error("High Energy Consumption Detected!")

    st.dataframe(result["anomalies"], use_container_width=True)
else:
    st.success("No abnormal energy consumption detected.")

st.divider()

# AI Recommendations
st.header("AI-Based Energy Saving Recommendations")

for recommendation in result["recommendations"]:
    st.write("- " + recommendation)

st.divider()

# Energy Records
st.header("Energy Consumption Records")
st.dataframe(df, use_container_width=True)

# Threshold
st.info(
    f"Anomaly Detection Threshold: {result['threshold']:.2f} kWh"
)

st.caption("Agentic FacilityOps AI - Milestone 1")
