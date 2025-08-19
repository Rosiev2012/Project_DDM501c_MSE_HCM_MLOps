#!/bin/bash

# Script chạy nhanh dự án MLOps
# Sử dụng: ./run_project.sh

echo "🚀 KHỞI ĐỘNG DỰ ÁN MLOPS"
echo "=========================="

# Kiểm tra Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 không được tìm thấy"
    exit 1
fi

# Tạo virtual environment (optional)
echo "📦 Tạo virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Cài đặt dependencies
echo "📚 Cài đặt dependencies..."
pip install -r requirements.txt

# Chạy ML pipeline
echo "🤖 Chạy ML Pipeline..."
python ml_pipeline.py

# Kiểm tra mô hình đã được tạo
if [ -f "models/best_model.pkl" ]; then
    echo "✅ Mô hình đã được tạo thành công!"
    
    # Chạy Flask app
    echo "🌐 Khởi động Flask Web App..."
    echo "📱 Truy cập: http://127.0.0.1:5000"
    python app.py
else
    echo "❌ Lỗi: Mô hình chưa được tạo"
    exit 1
fi
