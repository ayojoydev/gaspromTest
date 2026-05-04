# Project Summary

## Назначение

`Device Analytics Service` собирает телеметрию с устройств, хранит ее и предоставляет асинхронный анализ по устройству и пользователю.

## Что реализовано

- API на FastAPI
- PostgreSQL для хранения данных
- Celery и Redis для фоновой аналитики
- Docker Compose для локального окружения
- Locust-сценарий для нагрузки

## Основные сущности

- пользователь
- устройство
- показание
- результат анализа

## Основные операции

- создать пользователя
- создать устройство
- отправить одно показание
- отправить пакет показаний
- запустить анализ устройства
- получить результат анализа устройства
- запустить анализ пользователя
- получить результат анализа пользователя

## Документация

- [README.md](README.md)
- [QUICKSTART.md](QUICKSTART.md)
- [ARCHITECTURE.md](ARCHITECTURE.md)
- [TECHNICAL_REQUIREMENTS.md](TECHNICAL_REQUIREMENTS.md)
- [reports/load_tests/LOAD_TEST_RESULTS.md](reports/load_tests/LOAD_TEST_RESULTS.md)


