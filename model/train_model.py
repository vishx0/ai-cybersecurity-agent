import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

# -----------------------------
# 🔹 PATHS
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Dataset is inside model folder
DATA_PATH = os.path.join(BASE_DIR, "dataset.csv")

# Model save path
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

# -----------------------------
# 🔹 LOAD DATASET
# -----------------------------
try:
    df = pd.read_csv(DATA_PATH)
    print("✅ Dataset loaded successfully")
except Exception as e:
    print("❌ Error loading dataset:", e)
    exit()

# -----------------------------
# 🔹 FEATURES & LABEL
# -----------------------------
X = df[["open_ports", "risky_ports", "unknown_services"]]
y = df["label"]

# -----------------------------
# 🔹 TRAIN MODEL
# -----------------------------
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# -----------------------------
# 🔹 SAVE MODEL
# -----------------------------
try:
    joblib.dump(model, MODEL_PATH)
    print("✅ Model saved successfully")
    print(f"📁 Saved at: {MODEL_PATH}")
except Exception as e:
    print("❌ Error saving model:", e)

# -----------------------------
# 🔹 SUMMARY
# -----------------------------
print(f"📊 Training samples: {len(df)}")
print("🚀 Training complete")