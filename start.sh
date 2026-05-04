#!/bin/bash
# Quick start script for Device Analytics Service

set -e

echo "=========================================="
echo "Device Analytics Service - Quick Start"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}Docker is not installed. Please install Docker and Docker Compose.${NC}"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}Docker Compose is not installed. Please install Docker Compose.${NC}"
    exit 1
fi

echo -e "${BLUE}Starting Docker containers...${NC}"
docker-compose up -d

echo -e "${BLUE}Waiting for services to be ready...${NC}"
sleep 10

echo -e "${BLUE}Initializing database...${NC}"
docker-compose exec -T api python -c "from app.db.database import init_db; init_db(); print('Database initialized')"

echo ""
echo -e "${GREEN}=========================================="
echo "Services are ready!"
echo "==========================================${NC}"
echo ""
echo -e "${GREEN}API Endpoints:${NC}"
echo "  - Main API:  ${BLUE}http://localhost:8000${NC}"
echo "  - Swagger:   ${BLUE}http://localhost:8000/docs${NC}"
echo "  - ReDoc:     ${BLUE}http://localhost:8000/redoc${NC}"
echo ""
echo -e "${GREEN}Other Services:${NC}"
echo "  - Flower (Celery):  ${BLUE}http://localhost:5555${NC}"
echo "  - PostgreSQL:       ${BLUE}localhost:5432${NC}"
echo "  - Redis:            ${BLUE}localhost:6379${NC}"
echo ""
echo -e "${GREEN}Common Commands:${NC}"
echo "  - View logs:        ${BLUE}docker-compose logs -f${NC}"
echo "  - Stop services:    ${BLUE}docker-compose down${NC}"
echo "  - Run load test:    ${BLUE}bash run_load_test.sh${NC}"
echo ""
