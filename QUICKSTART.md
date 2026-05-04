# Quick Start

## Через Docker Compose

```bash
docker-compose up -d
docker-compose exec api python init_db.py
```

Проверка:

```bash
curl http://localhost:8000/api/health
```

Полезные адреса:

- `http://localhost:8000/docs`
- `http://localhost:8000/redoc`
- `http://localhost:5555`

## Локальный запуск без Docker

Нужны PostgreSQL и Redis.

```bash
poetry install
uvicorn app.main:app --host 0.0.0.0 --port 8000
celery -A app.tasks.celery_app worker --loglevel=info
```

## Нагрузочное тестирование

```bash
locust -f tests/locustfile.py --host=http://localhost:8000
```
