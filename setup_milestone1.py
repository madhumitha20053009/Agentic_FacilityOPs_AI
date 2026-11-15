from pathlib import Path
import shutil
import csv
import sqlite3

root = Path.cwd()

# Backup conflicting main.py folder
main_path = root / "main.py"
if main_path.is_dir():
    backup = root / "main.py_old_backup"
    if backup.exists():
        backup = root / "main.py_old_backup_2"
    shutil.move(str(main_path), str(backup))

# Backup existing Energy Agent code
agent = root / "agents" / "energy_agent.py"
if agent.exists():
    shutil.copy2(agent, root / "agents" / "energy_agent_old.py")

for folder in ["agents", "dashboard", "database", "data"]:
    (root / folder).mkdir(exist_ok=True)

# Sample energy dataset
csv_path = root / "data" / "energy_consumption.csv"
if not csv_path.exists():
    rows = [
        ["date", "energy_kwh"],
        ["2026-11-01", 120], ["2026-11-02", 125],
        ["2026-11-03", 118], ["2026-11-04", 130],
        ["2026-11-05", 122], ["2026-11-06", 128],
        ["2026-11-07", 124], ["2026-11-08", 119],
        ["2026-11-09", 126], ["2026-11-10", 123],
        ["2026-11-11", 121], ["2026-11-12", 127],
        ["2026-11-13", 260], ["2026-11-14", 125],
    ]
    with csv_path.open("w", newline="") as f:
        csv.writer(f).writerows(rows)

# Energy Agent
(root / "agents" / "energy_agent.py").write_text('''
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
''', encoding="utf-8")

# SQLite database
(root / "database" / "db.py").write_text('''
from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DB_FILE = ROOT / "database" / "energy.db"

def save_energy_data(df):
    with sqlite3.connect(DB_FILE) as conn:
        df.to_sql("energy_usage", conn, if_exists="replace", index=False)

def get_energy_data():
    with sqlite3.connect(DB_FILE) as conn:
        return pd.read_sql_query("SELECT * FROM energy_usage", conn)
''', encoding="utf-8")

# Streamlit dashboard
(root / "dashboard" / "app.py").write_text('''
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import streamlit as st
from agents.energy_agent import run_energy_agent
from database.db import save_energy_data

st.set_page_config(page_title="Facility Energy Intelligence", layout="wide")
st.title("Agentic FacilityOps AI")
st.subheader("Energy Intelligence & Monitoring Dashboard")

result = run_energy_agent()
df = result["data"]
save_energy_data(df)

c1, c2, c3 = st.columns(3)
c1.metric("Average Energy Usage", f"{result['average_usage']:.2f} kWh")
c2.metric("Total Energy Usage", f"{df['energy_kwh'].sum():.2f} kWh")
c3.metric("Detected Anomalies", len(result["anomalies"]))

st.subheader("Daily Energy Consumption")
st.line_chart(df.set_index("date")["energy_kwh"])

st.subheader("Energy Usage Data")
st.dataframe(df, use_container_width=True)

st.subheader("Anomaly Detection")
if result["anomalies"]:
    st.warning("Unusually high energy consumption detected.")
    st.dataframe(result["anomalies"], use_container_width=True)
else:
    st.success("No unusual energy consumption detected.")

st.subheader("AI-Based Energy Saving Recommendations")
for recommendation in result["recommendations"]:
    st.write("- " + recommendation)

st.caption("Demo uses sample energy data. Replace it with actual utility or IoT data for deployment.")
''', encoding="utf-8")

# Main entry point
(root / "main.py").write_text('''
import subprocess
import sys
from pathlib import Path

app = Path(__file__).resolve().parent / "dashboard" / "app.py"
subprocess.run([sys.executable, "-m", "streamlit", "run", str(app)], check=True)
''', encoding="utf-8")

(root / "requirements.txt").write_text(
    "pandas\\nstreamlit\\n", encoding="utf-8"
)

# Initialize database
sys_path = root / "database" / "db.py"
import importlib.util
spec = importlib.util.spec_from_file_location("db", sys_path)
db = importlib.util.module_from_spec(spec)
spec.loader.exec_module(db)
import pandas as pd
db.save_energy_data(pd.read_csv(csv_path))

print("Milestone 1 files created successfully!")
print("Created: agents/energy_agent.py")
print("Created: database/db.py and database/energy.db")
print("Created: data/energy_consumption.csv")
print("Created: dashboard/app.py")
print("Created: main.py and requirements.txt")
