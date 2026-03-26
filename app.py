import streamlit as st
import pandas as pd
import json

from backend.scanner import simulate_scan, real_scan
from backend.ai_agent import analyze
from utils.helpers import add_log, load_logs, calculate_risk_score

st.set_page_config(page_title="AI Cybersecurity Agent", layout="centered")

st.title("🛡️ AI Cybersecurity Agent Dashboard")

# -----------------------------
# 🔹 TARGET INPUT
# -----------------------------
target = st.text_input("Enter Target IP", "127.0.0.1")

# -----------------------------
# 🔹 SELECT MODE
# -----------------------------
scan_mode = st.radio(
    "Select Scan Mode",
    ["Simulated Scan", "Real Scan (Local Only)"]
)

# -----------------------------
# 🔹 RUN SCAN
# -----------------------------
if st.button("🔍 Run Security Scan"):

    # Choose scan mode
    if scan_mode == "Simulated Scan":
        scan_data = simulate_scan()
    else:
        scan_data = real_scan(target)

    # Handle errors
    if "error" in scan_data:
        st.error(f"Scan Error: {scan_data['error']}")
        st.stop()

    # AI Analysis
    result_data = analyze(scan_data)

    # Risk score
    risk_score = calculate_risk_score(scan_data)

    # Save log
    add_log(result_data)

    # -----------------------------
    # 🔹 DISPLAY RESULTS
    # -----------------------------
    st.subheader("📊 Scan Results")

    col1, col2, col3 = st.columns(3)

    col1.metric("Open Ports", scan_data["open_ports"])
    col2.metric("Risky Ports", scan_data["risky_ports"])
    col3.metric("Unknown Services", scan_data["unknown_services"])

    # -----------------------------
    st.subheader("🤖 AI Analysis")

    if result_data["result"] == "Threat Detected":
        st.error(f"🚨 {result_data['result']}")
    else:
        st.success(f"✅ {result_data['result']}")

    st.info(f"Confidence: {result_data['confidence']}%")

    # -----------------------------
    st.subheader("⚠️ Risk Score")

    st.write(f"{risk_score} / 100")
    st.progress(risk_score / 100)

    if risk_score > 70:
        st.error("🚨 High Risk System")
    elif risk_score > 40:
        st.warning("⚠ Medium Risk")
    else:
        st.success("✅ Low Risk")

# -----------------------------
# 🔹 LOAD LOGS
# -----------------------------
logs = load_logs()

st.subheader("📜 Scan History")

if logs:
    df = pd.DataFrame(logs)

    # Display last 5 logs
    for log in reversed(logs[-5:]):
        st.markdown(f"### 🕒 {log['time']}")

        col1, col2 = st.columns(2)
        col1.write(f"Result: {log['result']}")
        col2.write(f"Confidence: {log['confidence']}%")

        st.write(f"Data: {log['data']}")
        st.markdown("---")

    # -----------------------------
    # 🔹 CHARTS
    # -----------------------------
    st.subheader("📈 Confidence Trend")

    df["confidence"] = pd.to_numeric(df["confidence"])
    st.line_chart(df["confidence"])

    st.subheader("📊 Risk Distribution")
    counts = df["result"].value_counts()
    st.bar_chart(counts)

else:
    st.info("No scan history available")

# -----------------------------
# 🔹 DOWNLOAD LOGS (FIXED)
# -----------------------------
st.subheader("📥 Export Logs")

if logs:
    json_data = json.dumps(logs, indent=4)

    st.download_button(
        label="Download Logs (JSON)",
        data=json_data,
        file_name="scan_logs.json",
        mime="application/json"
    )

    # OPTIONAL CSV DOWNLOAD
    df = pd.DataFrame(logs)
    csv = df.to_csv(index=False)

    st.download_button(
        label="Download Logs (CSV)",
        data=csv,
        file_name="scan_logs.csv",
        mime="text/csv"
    )

else:
    st.info("No logs available to download")

# -----------------------------
# 🔹 HOW IT WORKS
# -----------------------------
st.subheader("ℹ️ How It Works")

st.write("""
- Network scan collects system data (simulated or real using Nmap)
- Features extracted: open ports, risky ports, unknown services
- Machine Learning model classifies threat level
- Risk score is calculated
- Logs are stored for tracking and analysis
- Optional blockchain integration for secure logging (local setup)
""")