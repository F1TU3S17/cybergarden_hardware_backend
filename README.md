# Hack Backend - IoT Device Monitoring System 🚀

> Система мониторинга и управления IoT устройствами на базе FastAPI с интеграцией AI для анализа данных

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-latest-green.svg)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)](https://www.sqlalchemy.org/)

## 📋 Описание

Hack Backend - это современный RESTful API сервис для мониторинга IoT устройств, сбора показаний датчиков и управления системой оповещений. Система поддерживает множество типов датчиков, реализует систему ролей пользователей, включает интеграцию с AI (Mistral) для интеллектуального анализа данных датчиков и предоставляет гибкий API для интеграции.

## ✨ Основные возможности

- 🔐 **Аутентификация и авторизация**
  - Регистрация и вход пользователей
  - Роли: администратор и оператор
  - Хеширование паролей (SHA-256)

- 📱 **Управление устройствами**
  - CRUD операции для IoT устройств
  - Отслеживание статуса и местоположения
  - Метаданные в формате JSON

- 📊 **Мониторинг датчиков**
  - Поддержка различных типов датчиков (температура, влажность, огонь и др.)
  - Хранение исторических данных
  - Временные метки для каждого измерения
  - Поддержка различных единиц измерения

- 🤖 **AI-анализ данных**
  - Интеграция с Mistral AI для интеллектуального анализа данных
  - Анализ показаний датчиков (температура, влажность, пожароопасность)
  - Автоматическое выявление аномалий и паттернов
  - Рекомендации по устранению проблем

- 🚨 **Система оповещений**
  - Создание и управление алертами
  - Уровни важности (low, medium, high, critical)
  - Статусы обработки (new, in_progress, resolved, closed)
  - Типы оповещений (temperature, humidity, motion, battery, fire, error)

- 🎛️ **Управление командами**
  - Отправка команд устройствам
  - Отслеживание статуса выполнения
  - Параметры команд в формате JSON

- 📝 **Blockchain-подобное логирование**
  - Цепочка хешей для обеспечения целостности
  - HMAC подписи
  - Защита от несанкционированного изменения данных

## 🏗️ Архитектура

```
hack_backend/
├── app/
│   ├── api/
│   │   └── v1/             # API маршруты версии 1
│   │       ├── alerts.py   # Эндпоинты оповещений
│   │       ├── analize.py  # AI-анализ данных датчиков
│   │       ├── auth.py     # Аутентификация
│   │       ├── devices.py  # Управление устройствами
│   │       ├── users.py    # Управление пользователями
│   │       └── commands.py # Команды устройствам
│   ├── core/
│   │   └── config.py       # Конфигурация приложения
│   ├── db/
│   │   └── session.py      # Настройки БД и сессии
│   ├── enums/              # Перечисления (статусы, типы, роли)
│   │   ├── action_type.py
│   │   ├── alert_status.py
│   │   ├── alert_type.py
│   │   ├── command_status.py
│   │   ├── device_status.py
│   │   ├── sensor_type.py
│   │   ├── timeframe.py
│   │   └── user_roles.py
│   ├── models/             # SQLAlchemy модели
│   │   ├── alert.py        # Модель оповещений
│   │   ├── command.py      # Модель команд
│   │   ├── device.py       # Модель устройств
│   │   ├── log.py          # Модель логов
│   │   ├── sensor_reading.py # Модель показаний датчиков
│   │   └── user.py         # Модель пользователей
│   └── service/
│       ├── gpt_service.py      # Сервис AI-анализа (Mistral)
│       └── password_service.py # Сервис работы с паролями
├── scripts/
│   └── init_db.py          # Скрипт инициализации БД
├── tests/                  # Тесты (в разработке)
├── index.html              # Главная страница
├── main.py                 # Точка входа приложения
├── requirements.txt        # Зависимости Python
└── README.md               # Документация
```

## 🚀 Быстрый старт

### Требования

- Python 3.13+ (или 3.9+)
- pip
- virtualenv (рекомендуется)
- API ключ Mistral AI (для функции AI-анализа)

### Установка

1. **Клонируйте репозиторий**
   ```bash
   git clone <repository-url>
   cd hack_backend
   ```

2. **Создайте виртуальное окружение**
   ```powershell
   # Windows
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   
   # Linux/Mac
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Установите зависимости**
   ```bash
   pip install -r requirements.txt
   ```

4. **Инициализируйте базу данных**
   ```bash
   python scripts/init_db.py
   ```

5. **Запустите сервер**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

6. **Откройте документацию API**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 📚 API Документация

### Основные эндпоинты

#### 🔐 Аутентификация (`/api/v1/auth`)

- `POST /login` - Вход в систему
- `POST /register` - Регистрация нового пользователя

#### 📱 Устройства (`/api/v1/devices`)

- `GET /devices` - Получить список устройств
- `GET /devices/{id}` - Получить устройство по ID
- `POST /devices` - Создать новое устройство
- `PATCH /devices/{id}` - Обновить устройство
- `DELETE /devices/{id}` - Удалить устройство
- `POST /devices/{id}/readings` - Добавить показание датчика
- `GET /devices/{id}/readings` - Получить показания датчиков

#### 🚨 Оповещения (`/api/v1/alerts`)

- `POST /alerts` - Создать оповещение
- `GET /alerts/{device_id}/alerts` - Получить оповещения устройства
- `PUT /alerts/{id}/status` - Обновить статус оповещения

#### 🎛️ Команды (`/api/v1/commands`)

- `POST /commands` - Отправить команду устройству

#### 👥 Пользователи (`/api/v1/users`)

- `GET /users/{id}` - Получить пользователя по ID

#### 🤖 AI-Анализ (`/api/v1/analyze`)

- `POST /analyze/gpt/{device_id}` - Анализ данных устройства с помощью AI
  - Анализирует последние 100 показаний датчиков
  - Обрабатывает данные по температуре, влажности и пожароопасности
  - Возвращает интеллектуальный анализ и рекомендации

## 🔧 Конфигурация

Создайте файл `.env` в корне проекта:

```env
PROJECT_NAME="My IoT Project"
DEBUG=True
DATABASE_URL="sqlite:///./test.db"
AI_API_KEY="your_mistral_api_key_here"
```

### Поддерживаемые параметры:

- `PROJECT_NAME` - Название проекта
- `DEBUG` - Режим отладки (True/False)
- `DATABASE_URL` - URL подключения к БД
- `AI_API_KEY` - API ключ для Mistral AI (требуется для функции анализа)

## 📊 Модели данных

### Device (Устройство)
```python
{
    "id": "abc123",
    "name": "Temperature Sensor 01",
    "location": "Warehouse A",
    "status": "active",
    "last_seen": "2025-10-04T12:00:00",
    "meta": {"model": "TMP36", "firmware": "1.2.3"}
}
```

### SensorReading (Показание датчика)
```python
{
    "id": "xyz789",
    "device_id": "abc123",
    "sensor_type": "temperature",
    "value": 23.5,
    "unit": "°C",
    "timestamp": "2025-10-04T12:00:00"
}
```

### Alert (Оповещение)
```python
{
    "id": "alert001",
    "device_id": "abc123",
    "alert_type": "temperature",
    "message": "Temperature exceeded threshold",
    "severity": "high",
    "status": "new",
    "acknowledged": false,
    "timestamp": "2025-10-04T12:00:00"
}
```

## 🔐 Безопасность

⚠️ **Важно для production:**

1. **Пароли**: Текущая реализация использует SHA-256 без salt. Для production замените на:
   ```python
   from passlib.hash import bcrypt
   # или
   from passlib.hash import argon2
   ```

2. **JWT токены**: Добавьте JWT для stateless аутентификации:
   ```python
   from jose import JWTError, jwt
   ```

3. **HTTPS**: Всегда используйте HTTPS в production

4. **Environment variables**: Храните секреты в переменных окружения

5. **Rate limiting**: Добавьте ограничение частоты запросов

## 🧪 Тестирование

```bash
# Установка тестовых зависимостей
pip install pytest httpx

# Запуск тестов
pytest tests/

# Запуск с покрытием кода
pytest --cov=app tests/
```

## 📝 Примеры использования

### Создание устройства

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/devices",
    params={
        "name": "Temperature Sensor 01",
        "location": "Warehouse A"
    }
)
device = response.json()
print(f"Device ID: {device['id']}")
```

### Добавление показания датчика

```python
response = requests.post(
    "http://localhost:8000/api/v1/devices/{device_id}/readings",
    json={
        "device_id": "abc123",
        "sensor_type": "temperature",
        "value": 23.5,
        "unit": "°C"
    }
)
reading = response.json()
```

### Создание оповещения

```python
response = requests.post(
    "http://localhost:8000/api/v1/alerts",
    json={
        "device_id": "abc123",
        "message": "Temperature too high!",
        "severity": "high",
        "alert_type": "temperature"
    }
)
alert = response.json()
```

### AI-анализ данных устройства

```python
response = requests.post(
    "http://localhost:8000/api/v1/analyze/gpt/abc123"
)
result = response.json()
print(f"Analysis: {result['analysis']}")
```

## 🛠️ Разработка

### Технологический стек

- **Backend Framework**: FastAPI
- **ORM**: SQLAlchemy 2.0+
- **Database**: SQLite (development), PostgreSQL (production ready)
- **AI Integration**: Mistral AI
- **HTTP Client**: httpx (для асинхронных запросов)
- **Configuration**: Pydantic Settings
- **Server**: Uvicorn

### Структура кода

- **Models** (`app/models/`): SQLAlchemy модели для БД
- **API Routes** (`app/api/v1/`): Эндпоинты REST API
- **Enums** (`app/enums/`): Перечисления и константы
- **Services** (`app/service/`): Бизнес-логика (пароли, AI-анализ)
- **Core** (`app/core/`): Конфигурация и общие компоненты
- **DB** (`app/db/`): Настройки базы данных

### Добавление нового типа датчика

1. Обновите `app/enums/sensor_type.py`:
   ```python
   class SensorType(str, Enum):
       TEMPERATURE = "temperature"
       HUMIDITY = "humidity"
       FIRE = "fire"
       PRESSURE = "pressure"  # Новый тип
   ```

2. Обработка показаний автоматически поддержит новый тип
3. При необходимости добавьте специфичную логику анализа в `GptService`

### Добавление нового типа оповещения

1. Обновите `app/enums/alert_type.py`:
   ```python
   class AlertType(str, Enum):
       TEMPERATURE = "temperature"
       FIRE = "fire"
       PRESSURE = "pressure"  # Новый тип
   ```

2. Система автоматически поддержит новый тип оповещений

## 📈 Production Checklist

- [ ] Замените SQLite на PostgreSQL/MySQL
- [ ] Внедрите bcrypt/Argon2 для паролей
- [ ] Добавьте JWT authentication
- [ ] Настройте CORS правильно для production
- [ ] Добавьте rate limiting
- [ ] Настройте структурированное логирование
- [ ] Добавьте мониторинг (Prometheus/Grafana)
- [ ] Настройте CI/CD pipeline
- [ ] Добавьте юнит-тесты и интеграционные тесты
- [ ] Настройте Docker и Docker Compose
- [ ] Настройте резервное копирование БД
- [ ] Добавьте health check эндпоинты
- [ ] Настройте SSL/TLS сертификаты
- [ ] Оптимизируйте запросы к БД (индексы, кэширование)
- [ ] Добавьте ограничение на использование AI API

## 🐳 Docker

### Dockerfile

```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование приложения
COPY . .

# Инициализация БД
RUN python scripts/init_db.py

# Запуск приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

EXPOSE 8000
```

### Docker Compose

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PROJECT_NAME=IoT Monitoring System
      - DEBUG=False
      - DATABASE_URL=postgresql://iot_user:iot_password@db:5432/iot_db
      - AI_API_KEY=${AI_API_KEY}
    depends_on:
      - db
    restart: unless-stopped
  
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: iot_db
      POSTGRES_USER: iot_user
      POSTGRES_PASSWORD: iot_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

volumes:
  postgres_data:
```

### Запуск с Docker

```bash
# Создайте файл .env с AI_API_KEY
echo "AI_API_KEY=your_mistral_api_key" > .env

# Соберите и запустите контейнеры
docker-compose up -d

# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down
```

## 📄 Лицензия

[Укажите лицензию проекта]

## 👥 Команда разработки

**Репозиторий**: [cybergarden_hardware_backend](https://github.com/F1TU3S17/cybergarden_hardware_backend)  
**Owner**: F1TU3S17  
**Branch**: main

## 🤝 Вклад

Мы приветствуем вклад в проект! Пожалуйста:

1. Fork репозиторий
2. Создайте feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit изменения (`git commit -m 'Add some AmazingFeature'`)
4. Push в branch (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## 📞 Поддержка

Если у вас возникли вопросы или проблемы:
- Создайте Issue в [GitHub репозитории](https://github.com/F1TU3S17/cybergarden_hardware_backend/issues)
- Ознакомьтесь с документацией API по адресу `/docs`

## 🔗 Полезные ссылки

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Mistral AI Documentation](https://docs.mistral.ai/)
- [Pydantic Documentation](https://d<img width="1920" height="1080" alt="2025-10-05_02-46-09" src="https://github.com/user-attachments/assets/27030b57-c2b8-4718-b40b-36de196e3b2d" />
ocs.pydantic.dev/)

---<img width="1920" height="1080" alt="2025-10-05_02-45-18" src="https://github.com/user-attachments/assets/c5745f96-027c-46f5-bbe5-99723edff2b5" />
<img width="1920" height="1080" alt="2025-10-05_02-45-36" src="https://github.com/user-attachments/assets/f90899ed-da61-41ca-b8dd-0a0e60ceb619" />
<img width="1920" height="1080" alt="2025-10-05_02-45-45" src="https://github.com/user-attachments/assets/6d231928-472e-49a1-9bfa-e7fb9e718062" />
<img width="1920" height="1080" alt="2025-10-05_02-45-57" src="https://github.com/user-attachments/assets/f9a3dc12-078b-41f4-9677-48e90a97804e" />
<img width="1920" height="1080" alt="2025-10-05_02-45-57" src="https://github.com/user-attachments/assets/9cfc4c85-ebc8-4d83-a0f1-0b9aae9a241c" />



Made with ❤️ using FastAPI, Python and AI

**Проект**: Cyber Garden Hackathon - Hardware Backend
