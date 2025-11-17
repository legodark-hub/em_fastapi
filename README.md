# API для Торговых Данных по Нефти

Этот проект представляет собой приложение на FastAPI, которое предоставляет API для доступа и анализа данных о торгах нефтью с биржи СПбМТСБ. Он использует базу данных PostgreSQL для хранения торговых данных и Redis для кэширования ответов API. Celery используется для фоновых задач, в частности для ежедневной очистки кэша.

## Возможности

*   Получение последних торговых дат.
*   Получение динамики торгов за заданный период и с учетом фильтров.
*   Получение результатов торгов на основе фильтров.
*   Кэширование ответов API для повышения производительности.
*   Асинхронные операции с базой данных.
*   Чистая и модульная структура проекта.

## Технологии

*   **Бэкенд:** FastAPI, Python
*   **База данных:** PostgreSQL, SQLAlchemy (с asyncpg)
*   **Кэширование:** Redis, fastapi-cache
*   **Очередь задач:** Celery
*   **Управление зависимостями:** pip
*   **Тестирование:** Pytest

## API Эндпоинты

*   `GET /api/trade/dates/`: Возвращает последние торговые даты.
*   `GET /api/trade/dynamics/`: Возвращает динамику торгов за заданный период и с учетом фильтров.
*   `GET /api/trade/result/`: Возвращает результаты торгов на основе фильтров.

## Начало Работы

### Требования

*   Python 3.10+
*   PostgreSQL
*   Redis

### Установка

1.  Клонируйте репозиторий:
    ```bash
    git clone https://github.com/legodark-hub/em_fastapi.git
    cd em_fastapi
    ```

2.  Создайте и активируйте виртуальное окружение:
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

4.  Создайте файл `.env` в корневом каталоге и добавьте следующие переменные окружения:
    ```
    MODE=DEV
    DB_NAME=your_db_name
    DB_HOST=localhost
    DB_PORT=5432
    DB_USER=your_db_user
    DB_PASS=your_db_password
    REDIS_HOST=localhost
    REDIS_PORT=6379
    ```

### Запуск Приложения

1.  Запустите приложение FastAPI:
    ```bash
    uvicorn main:app --reload
    ```

2.  Запустите воркер Celery:
    ```bash
    celery -A celery_app.celery_app worker --loglevel=info
    ```

3.  Запустите планировщик Celery beat:
    ```bash
    celery -A celery_app.celery_app beat --loglevel=info
    ```

## Запуск Тестов

Для запуска тестов используйте следующую команду:

```bash
pytest
```