#!/bin/bash

# Auto Deploy Script - Localhost CI/CD
# ===================================

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
DOCKER_USERNAME="YOUR_USERNAME"  # Thay bằng username thực
IMAGE_NAME="ml-model-api"
COMPOSE_FILE="docker-compose.yml"

echo -e "${BLUE}🚀 STARTING LOCALHOST DEPLOYMENT${NC}"
echo "=================================="

# Step 1: Pull latest image
echo -e "${YELLOW}📥 Pulling latest image from DockerHub...${NC}"
docker pull $DOCKER_USERNAME/$IMAGE_NAME:latest

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Image pulled successfully${NC}"
else
    echo -e "${RED}❌ Failed to pull image${NC}"
    exit 1
fi

# Step 2: Stop current services
echo -e "${YELLOW}⏹️  Stopping current services...${NC}"
docker-compose down

# Step 3: Start services with new image
echo -e "${YELLOW}🚀 Starting services with new image...${NC}"
docker-compose up -d

# Step 4: Wait for services to be ready
echo -e "${YELLOW}⏳ Waiting for services to start...${NC}"
sleep 15

# Step 5: Health checks
echo -e "${YELLOW}🏥 Performing health checks...${NC}"

# Check API
API_HEALTH=$(curl -s http://localhost:8000/api/health | grep -o '"status":"healthy"')
if [ ! -z "$API_HEALTH" ]; then
    echo -e "${GREEN}✅ API service is healthy${NC}"
else
    echo -e "${RED}❌ API service health check failed${NC}"
fi

# Check Web App
WEB_HEALTH=$(curl -s http://localhost:5001/health 2>/dev/null)
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Web app is running${NC}"
else
    echo -e "${YELLOW}⚠️  Web app not accessible (may be normal)${NC}"
fi

# Step 6: Show status
echo -e "${BLUE}📊 Deployment Status:${NC}"
docker-compose ps

echo ""
echo -e "${GREEN}🎉 DEPLOYMENT COMPLETED!${NC}"
echo "=================================="
echo -e "${BLUE}📱 Services available at:${NC}"
echo "🔗 API Service: http://localhost:8000/api/health"
echo "🌐 Web App: http://localhost:5001"
echo "📊 Service Status: docker-compose ps"
echo ""
echo -e "${BLUE}📋 Quick commands:${NC}"
echo "• View logs: docker-compose logs -f"
echo "• Stop services: docker-compose down"
echo "• Restart: docker-compose restart"
