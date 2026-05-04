# File Structure

## Каталоги

```text
app/
docker/
docs/
reports/
scripts/
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

reports/
  load_tests/
    LOAD_TEST_RESULTS.md
    <timestamp>/
      results_stats.csv
      results_failures.csv
      results_exceptions.csv
      results_stats_history.csv
      report.html
```

## Документация

```text
README.md
START_HERE.md
QUICKSTART.md
ARCHITECTURE.md
DEPLOYMENT.md
TECHNICAL_REQUIREMENTS.md
PROJECT_SUMMARY.md
PROJECT_COMPLETED.md
INDEX.md
```

## Скрипты

```text
scripts/
  init_db.py
  examples.py
  run_load_test.sh
  start.sh
  QUICKSTART_WINDOWS.sh
  worker.py
  celery_config.py
```
