# Deployment

## Локальное развертывание

Основной сценарий:

```bash
docker-compose up -d
docker-compose exec api python init_db.py
```

Проверка:

```bash
docker-compose ps
docker-compose logs api
docker-compose logs worker
```

## Переменные окружения

Основные параметры находятся в `.env`:

- `DATABASE_URL`
- `REDIS_URL`
- `CELERY_BROKER_URL`
- `CELERY_RESULT_BACKEND`
- `DEBUG`

## Остановка

```bash
docker-compose down
```

## Полезные команды

```bash
docker-compose restart api
docker-compose restart worker
docker-compose logs -f
```

## Замечания по эксплуатации

- PostgreSQL и Redis публикуются наружу на стандартные порты.
- API стартует на `8000`, Flower на `5555`.
- Для повторяемого запуска стоит проверять содержимое `.env` перед стартом.
