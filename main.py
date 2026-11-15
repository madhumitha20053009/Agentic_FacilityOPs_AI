
import subprocess
import sys
from pathlib import Path

app = Path(__file__).resolve().parent / "dashboard" / "app.py"
subprocess.run([sys.executable, "-m", "streamlit", "run", str(app)], check=True)
