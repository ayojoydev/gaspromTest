# File Structure

## Каталоги

```text
app/
docker/
tests/
```

## Приложение

```text
app/
  api/
    routes.py
  db/
    database.py
    models.py
  models/
    schemas.py
  services/
    data_service.py
  tasks/
    analytics.py
    celery_app.py
  config.py
  main.py
```

## Инфраструктура

```text
docker/
  Dockerfile

docker-compose.yml
.env
pyproject.toml
requirements.txt
```

## Тестирование

```text
tests/
  locustfile.py
```

## Документация

```text
README.md
START_HERE.md
QUICKSTART.md
ARCHITECTURE.md
DEPLOYMENT.md
TECHNICAL_REQUIREMENTS.md
LOAD_TEST_RESULTS.md
PROJECT_SUMMARY.md
PROJECT_COMPLETED.md
INDEX.md
```
