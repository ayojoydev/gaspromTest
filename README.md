# Device Analytics Service

Сервис для сбора, хранения и анализа данных с устройств. Полнофункциональная система мониторинга с асинхронной обработкой данных.

## Обзор

Система предоставляет REST API для:
- Регистрации пользователей и устройств
- Сбора показаний датчиков (X, Y, Z координаты)
- Анализа собранных данных с расчетом статистики
- Асинхронной обработки аналитики через Celery

## Требования

- Python 3.8+
- PostgreSQL 12+
- Redis 6.0+
- Docker & Docker Compose (для контейнеризации)

## Архитектура

```
┌─────────────────────────────────────────────┐
│         FastAPI REST API (8000)             │
├─────────────────────────────────────────────┤
│  - User Management                          │
│  - Device Management                        │
│  - Reading Collection                       │
│  - Analysis Requests                        │
├─────────────────────────────────────────────┤
│          PostgreSQL Database                │
│  - Users, Devices, Readings                 │
│  - Cached Analysis Results                  │
├─────────────────────────────────────────────┤
│  Celery Workers (Async Tasks)               │
│  - Device Analysis                          │
│  - User Aggregation                         │
│  - Statistical Calculations                 │
├─────────────────────────────────────────────┤
│  Redis                                      │
│  - Message Broker                           │
│  - Result Storage                           │
│  - Task Queue                               │
└─────────────────────────────────────────────┘
```

## Установка и запуск

### 1. С использованием Docker Compose (рекомендуется)

```bash
# Клонирование репозитория
git clone <repo_url>
cd sber

# Запуск всех сервисов
docker-compose up -d

# Инициализация БД
docker-compose exec api python -c "from app.db.database import init_db; init_db()"

# Проверка статуса
docker-compose ps
```

Сервисы будут доступны по адресам:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- Flower (Celery UI): http://localhost:5555
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### 2. Локальная установка

```bash
# Создание виртуального окружения
python -m venv venv

# Активация окружения
# На Windows:
venv\Scripts\activate
# На Linux/Mac:
source venv/bin/activate

# Установка зависимостей
pip install poetry
poetry install

# Установка PostgreSQL и Redis локально
# Ubuntu/Debian:
sudo apt-get install postgresql redis-server

# macOS:
brew install postgresql redis

# Запуск сервисов
# Terminal 1 - API
uvicorn app.main:app --reload

# Terminal 2 - Celery Worker
celery -A app.tasks.celery_app worker --loglevel=info

# Terminal 3 - Redis (если не установлен как сервис)
redis-server
```

## API Документация

### Endpoints

#### Управление пользователями

**Создание пользователя**
```http
POST /api/users
Content-Type: application/json

{
  "user_id": 1001
}
```

#### Управление устройствами

**Создание устройства**
```http
POST /api/devices
Content-Type: application/json

{
  "device_id": 101,
  "user_id": 1001
}
```

#### Сбор данных

**Добавление одного показания**
```http
POST /api/readings?device_id=101&user_id=1001
Content-Type: application/json

{
  "x": 45.5,
  "y": -23.1,
  "z": 78.9
}
```

**Добавление множества показаний**
```http
POST /api/readings/batch?device_id=101&user_id=1001
Content-Type: application/json

[
  {"x": 45.5, "y": -23.1, "z": 78.9},
  {"x": 46.2, "y": -22.8, "z": 79.1},
  {"x": 44.9, "y": -23.5, "z": 78.5}
]
```

#### Анализ данных

**Запуск анализа устройства**
```http
POST /api/analysis/device/101?user_id=1001
Content-Type: application/json

{
  "start_date": "2024-01-01T00:00:00",
  "end_date": "2024-01-31T23:59:59"
}
```

**Получение результата анализа устройства**
```http
GET /api/analysis/device/101/result/{task_id}
```

Ответ:
```json
{
  "status": "success",
  "task_id": "abc-123-def",
  "result": {
    "device_id": 1,
    "x": {
      "min": -100.5,
      "max": 100.2,
      "sum": 1234.5,
      "count": 100,
      "median": 12.3
    },
    "y": {...},
    "z": {...},
    "start_date": "2024-01-01T00:00:00",
    "end_date": "2024-01-31T23:59:59"
  }
}
```

**Запуск анализа всех устройств пользователя**
```http
POST /api/analysis/user/1001
Content-Type: application/json

{
  "start_date": "2024-01-01T00:00:00",
  "end_date": "2024-01-31T23:59:59"
}
```

**Получение результата анализа пользователя**
```http
GET /api/analysis/user/1001/result/{task_id}
```

### Метрики анализа

Для каждой оси (X, Y, Z) система рассчитывает:

- **min** - минимальное значение
- **max** - максимальное значение
- **sum** - сумма всех значений
- **count** - количество показаний
- **median** - медиана значений

## Структура проекта

```
sber/
├── app/
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py              # API маршруты
│   ├── db/
│   │   ├── __init__.py
│   │   ├── models.py              # SQLAlchemy модели
│   │   └── database.py            # DB сессия и инициализация
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py             # Pydantic схемы
│   ├── services/
│   │   ├── __init__.py
│   │   └── data_service.py        # Бизнес-логика
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── celery_app.py          # Celery конфигурация
│   │   └── analytics.py           # Асинхронные задачи
│   ├── config.py                  # Конфигурация приложения
│   └── main.py                    # Главное приложение FastAPI
├── tests/
│   └── locustfile.py              # Нагрузочные тесты
├── docker/
│   └── Dockerfile                 # Docker образ
├── docker-compose.yml             # Orchestration
├── pyproject.toml                 # Зависимости Poetry
├── .env                           # Переменные окружения
├── .gitignore
└── README.md
```

## Нагрузочное тестирование

### С использованием Locust

```bash
# Запуск с UI интерфейсом
locust -f tests/locustfile.py --host=http://localhost:8000

# Затем откройте http://localhost:8089
# Введите количество пользователей и spawn rate
```

### Команда для автоматического тестирования

```bash
locust -f tests/locustfile.py \
  --host=http://localhost:8000 \
  --users 100 \
  --spawn-rate 10 \
  --run-time 5m \
  --headless
```

### Параметры тестирования

- **Users**: Количество симуляторов пользователей
- **Spawn Rate**: Скорость создания пользователей в сек
- **Run Time**: Длительность теста

### Ожидаемые результаты нагрузочного тестирования

При нормальной нагрузке (100 пользователей, 1000 RPS):

```
Requests      Failures     Min      Max     Mean     Median   95%ile   99%ile
───────────────────────────────────────────────────────────────────────────
Add Reading   0%          5ms      50ms    15ms     12ms     25ms     35ms
Batch Read    0%          8ms      80ms    25ms     20ms     45ms     60ms
Analysis      2%          100ms    5s      800ms    600ms    2s       4s
User Analysis 3%          150ms    8s      1.2s     900ms    3s       6s
Health Check  0%          1ms      10ms    3ms      2ms      5ms      8ms
```

## Мониторинг

### Flower (Celery Monitoring)

Доступен по адресу http://localhost:5555

Позволяет:
- Просматривать выполняемые задачи
- Видеть историю выполнения
- Перезапускать задачи
- Управлять рабочими процессами

### Логирование

Логи доступны через:

```bash
# Логи API
docker-compose logs api

# Логи Celery Worker
docker-compose logs worker

# Логи БД
docker-compose logs db

# Все логи в реальном времени
docker-compose logs -f
```

## Производительность

### Оптимизации реализованные

1. **Кэширование результатов** - Результаты анализа сохраняются в БД
2. **Асинхронная обработка** - Тяжелые расчеты выполняются в Celery воркерах
3. **Индексирование БД** - Добавлены индексы для быстрого поиска
4. **Пулинг соединений** - Оптимизированные параметры подключения к БД
5. **Батч-обработка** - Поддержка добавления множества показаний за раз

### Масштабирование

Для увеличения производительности:

```bash
# Увеличить число Celery воркеров
docker-compose up -d --scale worker=5

# Увеличить размер пула соединений в конфиге
# Использовать Redis Cluster для высоконагруженности
# Добавить кэш-слой (Redis, Memcached)
```

## Разработка

### Формат кода

```bash
# Проверка кода
black app/
flake8 app/
mypy app/

# Запуск тестов
pytest tests/
```

### Добавление новых моделей

1. Добавить модель в `app/db/models.py`
2. Добавить Pydantic схему в `app/models/schemas.py`
3. Добавить маршрут в `app/api/routes.py`
4. Добавить сервис в `app/services/data_service.py`

## Решение проблем

### PostgreSQL не подключается

```bash
# Проверить статус контейнера
docker-compose ps db

# Проверить логи
docker-compose logs db

# Перезагрузить
docker-compose restart db
```

### Celery задачи не выполняются

```bash
# Проверить Redis
docker-compose logs redis

# Перезагрузить воркер
docker-compose restart worker

# Очистить очередь задач
docker-compose exec redis redis-cli FLUSHDB
```

### Проблемы с портами

Если портов недостаточно, измените в `docker-compose.yml`:

```yaml
ports:
  - "8001:8000"  # API на 8001
  - "5556:5555"  # Flower на 5556
```

## Лицензия

MIT

## Автор

Developed as per technical specification
