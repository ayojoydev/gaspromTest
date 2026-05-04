# Project Completed

Проект собран в виде сервиса для приема, хранения и анализа данных устройств.

## В состав репозитория входят

- исходный код приложения на FastAPI
- модели БД и сервисная логика
- Celery-задачи для фоновой аналитики
- Docker Compose-окружение
- сценарий нагрузочного тестирования
- комплект документации по запуску и структуре

## Полезные ссылки внутри репозитория

- [START_HERE.md](START_HERE.md)
- [README.md](README.md)
- [QUICKSTART.md](QUICKSTART.md)
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
- [TECHNICAL_REQUIREMENTS.md](TECHNICAL_REQUIREMENTS.md)

## Базовый запуск

```bash
docker-compose up -d
docker-compose exec api python init_db.py
```

## Что дальше

Если цель сейчас в аккуратной передаче проекта, обычно достаточно приложить ссылку на репозиторий, указать способ запуска и приложить [LOAD_TEST_RESULTS.md](LOAD_TEST_RESULTS.md).
