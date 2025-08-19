"""
MLOps Pipeline - CI Mode (Ultra Fast)
Optimized for <5min CI/CD build
"""

import time
start_time = time.time()

print("============================================================")
print("🚀 MLOps Pipeline - CI Mode (Fast)")
print("============================================================")

# Quick imports
import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import joblib
import json
import os

# Create models directory
os.makedirs('models', exist_ok=True)

print("\n📊 FAST MODE: Quick dataset & training")
print("--" * 25)

# Smaller dataset for CI speed
print("✅ Creating fast dataset...")
X, y = make_classification(
    n_samples=500,  # Reduced from 2000
    n_features=10,
    n_informative=8,
    n_redundant=2,
    n_clusters_per_class=1,
    random_state=42
)

# Quick split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
print(f"📈 Data split: {len(X_train)} train, {len(X_test)} test")

# Fast scaler
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Quick model - Random Forest (faster than XGBoost in CI)
print("\n🌳 Training Random Forest (CI optimized)...")
model = RandomForestClassifier(
    n_estimators=50,  # Reduced from 200
    max_depth=10,     # Limited depth
    random_state=42,
    n_jobs=-1        # Use all cores
)

model.fit(X_train_scaled, y_train)

# Quick evaluation
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)

print(f"📊 Model accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")

# Save models
print("\n💾 Saving models...")
joblib.dump(model, 'models/best_model.pkl')
joblib.dump(scaler, 'models/scaler.pkl')

# Model info
model_info = {
    "model_type": "RandomForest_CI",
    "accuracy": float(accuracy),
    "n_samples": len(X),
    "n_features": X.shape[1],
    "train_time": f"{time.time() - start_time:.2f}s",
    "optimized_for": "CI_speed"
}

with open('models/model_info.json', 'w') as f:
    json.dump(model_info, f, indent=2)

# Quick report
print(f"\n📋 Classification Report:")
print(classification_report(y_test, y_pred))

elapsed = time.time() - start_time
print("\n" + "=" * 60)
print(f"🎉 CI PIPELINE COMPLETED in {elapsed:.2f} seconds!")
print(f"✅ Model saved with {accuracy:.4f} accuracy")
print("=" * 60)
