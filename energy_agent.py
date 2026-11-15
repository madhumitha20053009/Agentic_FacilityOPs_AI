
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "energy_consumption.csv"

def run_energy_agent():
    df = pd.read_csv(DATA_FILE)
    df["energy_kwh"] = pd.to_numeric(df["energy_kwh"], errors="coerce")
    df = df.dropna(subset=["energy_kwh"])

    average = df["energy_kwh"].mean()
    std = df["energy_kwh"].std()
    threshold = average + std

    anomalies = df[df["energy_kwh"] > threshold].to_dict("records")

    recommendations = []
    if anomalies:
        recommendations.append("Check equipment operating on high-consumption days.")
    recommendations.append("Switch off unused lights and electrical equipment.")
    recommendations.append("Monitor HVAC usage and maintain suitable temperature settings.")
    recommendations.append("Compare daily energy usage to identify unusual increases.")

    return {
        "data": df,
        "average_usage": average,
        "anomalies": anomalies,
        "recommendations": recommendations,
        "threshold": threshold
    }
