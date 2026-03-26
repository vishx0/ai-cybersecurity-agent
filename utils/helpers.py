import json
import os
from datetime import datetime

# Path to logs file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, "logs", "scan_logs.json")


# -----------------------------
# 🔹 LOAD LOGS
# -----------------------------
def load_logs():
    try:
        if not os.path.exists(LOG_FILE):
            return []

        with open(LOG_FILE, "r") as f:
            return json.load(f)

    except Exception:
        return []


# -----------------------------
# 🔹 SAVE LOGS
# -----------------------------
def save_logs(logs):
    try:
        with open(LOG_FILE, "w") as f:
            json.dump(logs, f, indent=4)
    except Exception as e:
        print("Error saving logs:", e)


# -----------------------------
# 🔹 ADD NEW LOG ENTRY
# -----------------------------
def add_log(result_data):
    logs = load_logs()

    new_entry = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "result": result_data.get("result"),
        "confidence": result_data.get("confidence"),
        "data": result_data.get("details")
    }

    logs.append(new_entry)
    save_logs(logs)


# -----------------------------
# 🔹 RISK SCORE CALCULATION
# -----------------------------
def calculate_risk_score(scan_data):
    open_ports = scan_data.get("open_ports", 0)
    risky_ports = scan_data.get("risky_ports", 0)
    unknown_services = scan_data.get("unknown_services", 0)

    # Simple weighted scoring
    score = (open_ports * 1.5) + (risky_ports * 3) + (unknown_services * 2)

    # Normalize to 0–100
    score = min(score, 100)

    return round(score, 2)