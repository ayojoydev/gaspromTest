# Device Analytics Service

Сервис собирает показания устройств в формате `{"x": float, "y": float, "z": float}`, сохраняет их в PostgreSQL и запускает асинхронный анализ через Celery и Redis.

Проект собран на `FastAPI`, разворачивается через `Docker Compose` и содержит сценарий нагрузочного тестирования на `Locust`.

## Что есть в проекте

- REST API для пользователей, устройств и показаний
- Хранение данных в PostgreSQL
- Асинхронные задачи аналитики через Celery
- Redis как брокер и backend результатов
- Docker Compose для локального запуска
- Locust-сценарий для нагрузочного тестирования

## Стек

- Python 3.11 в Docker
- FastAPI
- SQLAlchemy
- PostgreSQL
- Celery
- Redis
- Locust

## Структура

- [START_HERE.md](START_HERE.md) - короткий маршрут по проекту
- [QUICKSTART.md](QUICKSTART.md) - быстрый запуск
- [ARCHITECTURE.md](ARCHITECTURE.md) - архитектура и компоненты
- [TECHNICAL_REQUIREMENTS.md](TECHNICAL_REQUIREMENTS.md) - сверка с ТЗ
- [reports/load_tests/LOAD_TEST_RESULTS.md](reports/load_tests/LOAD_TEST_RESULTS.md) - результаты нагрузочного тестирования
- [DEPLOYMENT.md](DEPLOYMENT.md) - запуск и эксплуатация
- [FILE_STRUCTURE.md](FILE_STRUCTURE.md) - структура каталогов
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - краткая сводка проекта

## Быстрый запуск

```bash
docker-compose up -d
docker compose exec api python scripts/init_db.py
```

После запуска будут доступны:

- API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Flower: `http://localhost:5555`

## Основные endpoints

- `POST /api/users`
- `POST /api/devices`
- `POST /api/readings`
- `POST /api/readings/batch`
- `POST /api/analysis/device/{device_id}`
- `GET /api/analysis/device/{device_id}/result/{task_id}`
- `POST /api/analysis/user/{user_id}`
- `GET /api/analysis/user/{user_id}/result/{task_id}`
- `GET /api/health`

## Пример запроса

```http
POST /api/readings?device_id=101&user_id=1001
Content-Type: application/json

{
  "x": 12.4,
  "y": -3.8,
  "z": 9.1
}
```

## Нагрузочное тестирование

Locust-сценарий находится в [tests/locustfile.py](tests/locustfile.py).

Запуск:

```bash
bash scripts/run_load_test.sh
```

Сводка по зафиксированным результатам находится в [reports/load_tests/LOAD_TEST_RESULTS.md](reports/load_tests/LOAD_TEST_RESULTS.md).

