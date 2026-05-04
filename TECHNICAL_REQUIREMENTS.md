# Соответствие ТЗ

Документ показывает, как проект соотносится с техническим заданием в текущем состоянии репозитория.

## Функциональные требования

### 1. Сбор статистики с устройства

Реализовано.

- Формат данных: `{"x": float, "y": float, "z": float}`
- Endpoint: `POST /api/readings`
- Batch endpoint: `POST /api/readings/batch`
- Сохранение в БД: таблица `readings`

Связанные файлы:

- [app/api/routes.py](app/api/routes.py)
- [app/models/schemas.py](app/models/schemas.py)
- [app/services/data_service.py](app/services/data_service.py)
- [app/db/models.py](app/db/models.py)

### 2. Анализ статистики за период и за все время

Реализовано.

- Анализ устройства запускается через `POST /api/analysis/device/{device_id}`
- Период задается через `start_date` и `end_date`
- Если даты не переданы, анализ идет по всем данным

Связанные файлы:

- [app/api/routes.py](app/api/routes.py)
- [app/tasks/analytics.py](app/tasks/analytics.py)

### 3. Метрики анализа

Реализовано.

Для каждой оси считаются:

- минимальное значение
- максимальное значение
- количество
- сумма
- медиана

Связанные файлы:

- [app/tasks/analytics.py](app/tasks/analytics.py)
- [app/models/schemas.py](app/models/schemas.py)

### 4. Добавление пользователей устройств

Реализовано.

- Endpoint: `POST /api/users`
- Привязка устройства к пользователю: `POST /api/devices`

Связанные файлы:

- [app/api/routes.py](app/api/routes.py)
- [app/services/data_service.py](app/services/data_service.py)
- [app/db/models.py](app/db/models.py)

### 5. Анализ показаний устройств по идентификатору пользователя

Реализовано частично.

Что есть:

- запуск аналитики по пользователю
- агрегированные результаты по всем устройствам пользователя

Что требует проверки или доработки:

- отдельная статистика по каждому устройству в ответе сейчас документально ожидается, но текущая реализация возвращает не полный per-device разрез

Связанные файлы:

- [app/api/routes.py](app/api/routes.py)
- [app/tasks/analytics.py](app/tasks/analytics.py)

## Нефункциональные требования

### REST

Реализовано.

### FastAPI

Реализовано.

### Хранение данных в БД

Реализовано на PostgreSQL.

### Асинхронная аналитика через Celery

Реализовано, но стоит отдельно проверить регистрацию задач в worker-процессе при запуске через `docker-compose`.

### Нагрузочное тестирование через Locust

Сценарий реализован.

Файлы:

- [tests/locustfile.py](tests/locustfile.py)
- [LOAD_TEST_RESULTS.md](LOAD_TEST_RESULTS.md)

### Docker и Docker Compose

Реализовано.

Файлы:

- [docker/Dockerfile](docker/Dockerfile)
- [docker-compose.yml](docker-compose.yml)

## Итог

Проект закрывает основную часть ТЗ по архитектуре и базовой функциональности. Для строгой сдачи без оговорок стоит дополнительно синхронизировать пользовательскую аналитику с формулировкой ТЗ и проверить рабочий контур Celery.
