# Start Here

Если нужно быстро понять проект, идите в таком порядке:

1. Откройте [README.md](README.md), чтобы увидеть общую картину.
2. Пройдите [QUICKSTART.md](QUICKSTART.md), чтобы поднять сервис локально.
3. Проверьте [TECHNICAL_REQUIREMENTS.md](TECHNICAL_REQUIREMENTS.md), если нужна сверка с ТЗ.
4. Посмотрите [ARCHITECTURE.md](ARCHITECTURE.md), если интересует устройство сервиса.
5. Откройте [reports/load_tests/LOAD_TEST_RESULTS.md](reports/load_tests/LOAD_TEST_RESULTS.md), если нужны результаты нагрузки.

## Минимальный сценарий запуска

```bash
docker-compose up -d
docker compose exec api python scripts/init_db.py
```

После этого откройте `http://localhost:8000/docs`.
