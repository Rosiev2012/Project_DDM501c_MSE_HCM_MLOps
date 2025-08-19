# DockerHub Setup and Push Script
# ================================

#!/bin/bash

echo "🐳 DOCKERHUB SETUP AND PUSH SCRIPT"
echo "=================================="

# Cấu hình (thay đổi theo thông tin của bạn)
DOCKERHUB_USERNAME="your-dockerhub-username"
IMAGE_NAME="ml-model-api"
VERSION="v1.0"

# Màu sắc cho output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function để in màu
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Kiểm tra Docker
if ! command -v docker &> /dev/null; then
    print_error "Docker chưa được cài đặt!"
    exit 1
fi

print_status "Docker đã được cài đặt"

# Kiểm tra đăng nhập DockerHub
echo "🔐 Checking DockerHub login..."
if ! docker info | grep -q "Username"; then
    print_warning "Chưa đăng nhập DockerHub. Hãy chạy: docker login"
    read -p "Bạn có muốn đăng nhập ngay bây giờ? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker login
    else
        print_error "Cần đăng nhập DockerHub để tiếp tục!"
        exit 1
    fi
fi

print_status "Đã đăng nhập DockerHub"

# Build image
echo "🏗️  Building Docker image..."
if docker build -t $IMAGE_NAME:$VERSION .; then
    print_status "Build thành công"
else
    print_error "Build thất bại!"
    exit 1
fi

# Tag cho DockerHub
echo "🏷️  Tagging image for DockerHub..."
docker tag $IMAGE_NAME:$VERSION $DOCKERHUB_USERNAME/$IMAGE_NAME:$VERSION
docker tag $IMAGE_NAME:$VERSION $DOCKERHUB_USERNAME/$IMAGE_NAME:latest

print_status "Tagged image successfully"

# Push to DockerHub
echo "📤 Pushing to DockerHub..."
if docker push $DOCKERHUB_USERNAME/$IMAGE_NAME:$VERSION; then
    print_status "Pushed version $VERSION successfully"
else
    print_error "Push version thất bại!"
    exit 1
fi

if docker push $DOCKERHUB_USERNAME/$IMAGE_NAME:latest; then
    print_status "Pushed latest tag successfully"
else
    print_error "Push latest thất bại!"
    exit 1
fi

# Thông tin hoàn thành
echo ""
echo "🎉 HOÀN THÀNH!"
echo "=================================="
echo "📦 Image: $DOCKERHUB_USERNAME/$IMAGE_NAME:$VERSION"
echo "🔗 DockerHub URL: https://hub.docker.com/r/$DOCKERHUB_USERNAME/$IMAGE_NAME"
echo ""
echo "📋 Để chạy container:"
echo "docker run -p 8000:8000 $DOCKERHUB_USERNAME/$IMAGE_NAME:$VERSION"
echo ""
echo "🚀 Để deploy với docker-compose:"
echo "docker-compose up -d"
