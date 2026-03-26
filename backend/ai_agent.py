import joblib
import os

# -----------------------------
# 🔹 PATH SETUP
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "model", "model.pkl")

# -----------------------------
# 🔹 LOAD MODEL
# -----------------------------
try:
    model = joblib.load(MODEL_PATH)
    print("✅ Model loaded successfully")
except Exception as e:
    print("❌ Error loading model:", e)
    model = None


# -----------------------------
# 🔹 ANALYZE FUNCTION
# -----------------------------
def analyze(scan_data):

    if model is None:
        return {
            "result": "Model not loaded",
            "confidence": 0,
            "details": scan_data
        }

    # Extract features
    open_ports = scan_data.get("open_ports", 0)
    risky_ports = scan_data.get("risky_ports", 0)
    unknown_services = scan_data.get("unknown_services", 0)

    features = [[open_ports, risky_ports, unknown_services]]

    try:
        # Prediction
        prediction = model.predict(features)[0]

        # 🔥 FIXED CONFIDENCE
        probabilities = model.predict_proba(features)[0]
        probability = max(probabilities)

        result = "Threat Detected" if prediction == 1 else "Safe"

        return {
            "result": result,
            "confidence": round(probability * 100, 2),
            "details": scan_data
        }

    except Exception as e:
        return {
            "result": "Error during analysis",
            "confidence": 0,
            "error": str(e),
            "details": scan_data
        }