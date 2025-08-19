# =====================================================
# Dự án MLOps: Phân loại nhị phân với Machine Learning
# =====================================================

import pandas as pd
import numpy as np
import json
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
from xgboost import XGBClassifier
import joblib
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("🚀 DỰ ÁN MLOS: PHÂN LOẠI NHỊ PHÂN")
print("="*60)

# =====================================================
# BƯỚC 1: TẠO DỮ LIỆU VÀ MÔ HÌNH ĐỠN GIẢN NHẤT
# =====================================================

print("\n📊 BƯỚC 1: Tạo dữ liệu và mô hình cơ bản")
print("-" * 50)

# Tạo dữ liệu synthetic
X, y = make_classification(
    n_samples=1000,      # Số lượng mẫu
    n_features=10,       # Số đặc trưng
    n_informative=8,     # Số đặc trưng có ý nghĩa
    n_redundant=2,       # Số đặc trưng dư thừa
    random_state=42      # Đảm bảo tái hiện
)

print(f"✅ Đã tạo dữ liệu: {X.shape[0]} mẫu, {X.shape[1]} đặc trưng")
print(f"📈 Phân phối lớp: {np.bincount(y)}")

# Chia dữ liệu
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

print(f"🔄 Chia dữ liệu: Training {X_train.shape[0]}, Testing {X_test.shape[0]}")

# 1.1 Mô hình đơn giản nhất: Logistic Regression
print("\n🎯 Mô hình 1: Logistic Regression (Cơ bản)")
simple_model = LogisticRegression(random_state=42)
simple_model.fit(X_train, y_train)

y_pred_simple = simple_model.predict(X_test)
accuracy_simple = accuracy_score(y_test, y_pred_simple)

print(f"📊 Độ chính xác: {accuracy_simple:.4f} ({accuracy_simple*100:.2f}%)")
print("📋 Báo cáo chi tiết:")
print(classification_report(y_test, y_pred_simple))

# =====================================================
# BƯỚC 2: THỬ NGHIỆM TUNING SIÊU THAM SỐ
# =====================================================

print("\n🔧 BƯỚC 2: Tuning siêu tham số")
print("-" * 50)

# 2.1 Tuning Logistic Regression
print("\n⚙️ Tuning Logistic Regression...")
param_grid_lr = {
    'C': [0.01, 0.1, 1, 10, 100],
    'solver': ['liblinear', 'lbfgs'],
    'max_iter': [100, 200, 500]
}

grid_search_lr = GridSearchCV(
    estimator=LogisticRegression(random_state=42),
    param_grid=param_grid_lr,
    scoring='accuracy',
    cv=5,
    verbose=0
)

grid_search_lr.fit(X_train, y_train)
best_lr_model = grid_search_lr.best_estimator_

y_pred_lr_tuned = best_lr_model.predict(X_test)
accuracy_lr_tuned = accuracy_score(y_test, y_pred_lr_tuned)

print(f"🏆 Tham số tốt nhất: {grid_search_lr.best_params_}")
print(f"📊 Độ chính xác sau tuning: {accuracy_lr_tuned:.4f} ({accuracy_lr_tuned*100:.2f}%)")

# =====================================================
# BƯỚC 3: THÊEM DỮ LIỆU VÀ MÔ HÌNH PHỨC TẠP HƠN
# =====================================================

print("\n📈 BƯỚC 3: Làm giàu dữ liệu và thử mô hình khác")
print("-" * 50)

# 3.1 Tạo dữ liệu lớn hơn và chuẩn hóa
X_large, y_large = make_classification(
    n_samples=2000,
    n_features=10,
    n_informative=8,
    n_redundant=2,
    random_state=42
)

# Thêm nhiễu và chuẩn hóa
noise = np.random.normal(0, 0.1, X_large.shape)
X_noisy = X_large + noise

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_noisy)

X_train_large, X_test_large, y_train_large, y_test_large = train_test_split(
    X_scaled, y_large, test_size=0.3, random_state=42
)

print(f"✅ Dữ liệu mở rộng: {X_train_large.shape[0]} training, {X_test_large.shape[0]} testing")

# 3.2 Random Forest
print("\n🌳 Mô hình 2: Random Forest")
rf_model = RandomForestClassifier(random_state=42, n_estimators=100)
rf_model.fit(X_train_large, y_train_large)

y_pred_rf = rf_model.predict(X_test_large)
accuracy_rf = accuracy_score(y_test_large, y_pred_rf)

print(f"📊 Độ chính xác Random Forest: {accuracy_rf:.4f} ({accuracy_rf*100:.2f}%)")

# 3.3 Tuning Random Forest
print("\n⚙️ Tuning Random Forest...")
param_grid_rf = {
    'n_estimators': [50, 100, 200],
    'max_depth': [10, 20, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

grid_search_rf = GridSearchCV(
    estimator=RandomForestClassifier(random_state=42),
    param_grid=param_grid_rf,
    scoring='accuracy',
    cv=3,
    verbose=0
)

grid_search_rf.fit(X_train_large, y_train_large)
best_rf_model = grid_search_rf.best_estimator_

y_pred_rf_tuned = best_rf_model.predict(X_test_large)
accuracy_rf_tuned = accuracy_score(y_test_large, y_pred_rf_tuned)

print(f"🏆 Tham số tốt nhất RF: {grid_search_rf.best_params_}")
print(f"📊 Độ chính xác RF sau tuning: {accuracy_rf_tuned:.4f} ({accuracy_rf_tuned*100:.2f}%)")

# 3.4 XGBoost
print("\n🚀 Mô hình 3: XGBoost")
xgb_model = XGBClassifier(
    random_state=42,
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    eval_metric='logloss'
)
xgb_model.fit(X_train_large, y_train_large)

y_pred_xgb = xgb_model.predict(X_test_large)
accuracy_xgb = accuracy_score(y_test_large, y_pred_xgb)

print(f"📊 Độ chính xác XGBoost: {accuracy_xgb:.4f} ({accuracy_xgb*100:.2f}%)")

# =====================================================
# BƯỚC 4: SO SÁNH KẾT QUẢ CÁC MÔ HÌNH
# =====================================================

print("\n📊 BƯỚC 4: So sánh kết quả các mô hình")
print("=" * 60)

# Tạo bảng so sánh
results = {
    'Mô hình': ['Logistic Regression', 'LR (Tuned)', 'Random Forest', 'RF (Tuned)', 'XGBoost'],
    'Accuracy': [accuracy_simple, accuracy_lr_tuned, accuracy_rf, accuracy_rf_tuned, accuracy_xgb],
    'Accuracy (%)': [f"{accuracy_simple*100:.2f}%", f"{accuracy_lr_tuned*100:.2f}%", 
                     f"{accuracy_rf*100:.2f}%", f"{accuracy_rf_tuned*100:.2f}%", f"{accuracy_xgb*100:.2f}%"]
}

df_results = pd.DataFrame(results)
print(df_results.to_string(index=False))

# Tìm mô hình tốt nhất
best_accuracy = max(accuracy_simple, accuracy_lr_tuned, accuracy_rf, accuracy_rf_tuned, accuracy_xgb)
if best_accuracy == accuracy_xgb:
    best_model = xgb_model
    best_model_name = "XGBoost"
elif best_accuracy == accuracy_rf_tuned:
    best_model = best_rf_model
    best_model_name = "Random Forest (Tuned)"
else:
    best_model = best_lr_model
    best_model_name = "Logistic Regression (Tuned)"

print(f"\n🏆 MÔ HÌNH TỐT NHẤT: {best_model_name}")
print(f"📊 Độ chính xác: {best_accuracy:.4f} ({best_accuracy*100:.2f}%)")

# =====================================================
# BƯỚC 5: LƯU MÔ HÌNH TỐT NHẤT
# =====================================================

print(f"\n💾 BƯỚC 5: Lưu mô hình tốt nhất")
print("-" * 50)

# Lưu mô hình
model_path = "models/best_model.pkl"
joblib.dump(best_model, model_path)
print(f"✅ Đã lưu mô hình tại: {model_path}")

# Lưu scaler (quan trọng cho việc deploy)
scaler_path = "models/scaler.pkl"
joblib.dump(scaler, scaler_path)
print(f"✅ Đã lưu scaler tại: {scaler_path}")

# Lưu thông tin mô hình
model_info = {
    'model_name': best_model_name,
    'accuracy': best_accuracy,
    'features': X.shape[1],
    'training_samples': X_train_large.shape[0]
}

with open('models/model_info.json', 'w') as f:
    json.dump(model_info, f, indent=2)
print(f"✅ Đã lưu thông tin mô hình tại: models/model_info.json")

# Báo cáo chi tiết mô hình tốt nhất
print(f"\n📋 BÁO CÁO CHI TIẾT MÔ HÌNH TỐT NHẤT")
print("-" * 50)
y_best_pred = best_model.predict(X_test_large)
print(classification_report(y_test_large, y_best_pred))

print("\n" + "="*60)
print("🎉 HOÀN THÀNH PHẦN MACHINE LEARNING!")
print("📝 Tiếp theo: Tạo Flask Web App")
print("="*60)
