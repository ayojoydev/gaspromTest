#!/bin/bash

echo "Device Analytics Service - Quick Start"
echo "======================================"
echo ""

if ! command -v docker >/dev/null 2>&1; then
    echo "Docker is not installed."
    exit 1
fi

if ! command -v docker-compose >/dev/null 2>&1; then
    echo "Docker Compose is not installed."
    exit 1
fi

echo "Starting services..."
docker-compose up -d

if [ $? -eq 0 ]; then
    echo ""
    echo "Initializing database..."
    sleep 5
    docker-compose exec -T api python scripts/init_db.py
    echo ""
    echo "Service URLs:"
    echo "  API:     http://localhost:8000"
    echo "  Swagger: http://localhost:8000/docs"
    echo "  ReDoc:   http://localhost:8000/redoc"
    echo "  Flower:  http://localhost:5555"
    echo ""
    echo "Useful commands:"
    echo "  docker-compose logs -f"
    echo "  docker-compose down"
    echo "  python scripts/examples.py"
else
    echo "Failed to start services."
    exit 1
fi
