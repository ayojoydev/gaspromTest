#!/bin/bash
# Device Analytics Service - Windows Quick Start Guide
# Это руководство для быстрого запуска сервиса на Windows

echo "Device Analytics Service - Quick Start"
echo "======================================"
echo ""

# Проверить наличие Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен!"
    echo "Пожалуйста, установите Docker Desktop с сайта: https://www.docker.com/products/docker-desktop"
    exit 1
fi

echo "✓ Docker обнаружен"

# Проверить наличие Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен!"
    exit 1
fi

echo "✓ Docker Compose обнаружен"
echo ""

echo "Запуск сервисов..."
echo "  1️⃣  PostgreSQL (5432)"
echo "  2️⃣  Redis (6379)"
echo "  3️⃣  API (8000)"
echo "  4️⃣  Celery Worker"
echo "  5️⃣  Flower (5555)"
echo ""

docker-compose up -d

if [ $? -eq 0 ]; then
    echo "✓ Все сервисы запущены!"
    echo ""
    echo "Инициализация БД..."
    sleep 5
    
    docker-compose exec -T api python init_db.py
    
    echo ""
    echo "=========================================="
    echo "✅ ГОТОВО! Сервис работает:"
    echo "=========================================="
    echo ""
    echo "📡 API:        http://localhost:8000"
    echo "📚 Swagger:    http://localhost:8000/docs"
    echo "📖 ReDoc:      http://localhost:8000/redoc"
    echo "🌸 Flower:     http://localhost:5555"
    echo ""
    echo "💾 PostgreSQL: localhost:5432"
    echo "   User: postgres"
    echo "   Pass: postgres"
    echo ""
    echo "Redis:        localhost:6379"
    echo ""
    echo "Полезные команды:"
    echo "  docker-compose logs -f          - просмотр логов"
    echo "  docker-compose down             - остановка сервисов"
    echo "  python examples.py              - примеры использования API"
    echo ""
else
    echo "❌ Ошибка при запуске сервисов!"
    exit 1
fi
