import pandas as pd
from pathlib import Path
from sklearn.metrics import accuracy_score, classification_report

# Normal energy readings for baseline
baseline = pd.Series([100, 110, 120, 130, 140])
threshold = baseline.mean() + 2 * baseline.std()

# Test dataset with known labels
normal = [100,110,120,130,140] * 4
anomalies = [200,220,240,260,280]

df = pd.DataFrame({
    "energy_kwh": normal + anomalies,
    "actual": [0] * len(normal) + [1] * len(anomalies)
})

df["predicted"] = (df["energy_kwh"] > threshold).astype(int)

Path("data").mkdir(exist_ok=True)
df.to_csv("data/anomaly_test.csv", index=False)

accuracy = accuracy_score(df["actual"], df["predicted"]) * 100

print("===== ANOMALY DETECTION EVALUATION =====")
print("Threshold:", round(threshold, 2), "kWh")
print("Test records:", len(df))
print("Correct predictions:", (df["actual"] == df["predicted"]).sum())
print("Accuracy:", round(accuracy, 2), "%")
print(classification_report(
    df["actual"], df["predicted"],
    target_names=["Normal", "Anomaly"],
    zero_division=0
))
