# Hack Backend - IoT Device Monitoring System 🚀

> Система мониторинга и управления IoT устройствами на базе FastAPI

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-red.svg)](https://www.sqlalchemy.org/)

## 📋 Описание

Hack Backend - это RESTful API сервис для мониторинга IoT устройств, сбора показаний датчиков и управления системой оповещений. Система поддерживает множество типов датчиков, реализует систему ролей пользователей и предоставляет гибкий API для интеграции.

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
  - Поддержка различных типов датчиков (температура, влажность, и др.)
  - Хранение исторических данных
  - Временные метки для каждого измерения

- 🚨 **Система оповещений**
  - Создание и управление алертами
  - Уровни важности (low, medium, high, critical)
  - Статусы обработки (new, in_progress, resolved, closed)
  - Типы оповещений (temperature, humidity, motion, battery, error)

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
│   │   ├── enums/          # Перечисления (статусы, типы, роли)
│   │   └── v1/             # API маршруты версии 1
│   │       ├── alerts.py   # Эндпоинты оповещений
│   │       ├── auth.py     # Аутентификация
│   │       ├── devices.py  # Управление устройствами
│   │       ├── users.py    # Управление пользователями
│   │       └── commads.py  # Команды устройствам
│   ├── core/
│   │   └── config.py       # Конфигурация приложения
│   ├── db/
│   │   └── session.py      # Настройки БД и сессии
│   ├── models/             # SQLAlchemy модели
│   │   ├── alert.py        # Модель оповещений
│   │   ├── command.py      # Модель команд
│   │   ├── device.py       # Модель устройств
│   │   ├── log.py          # Модель логов
│   │   ├── sensor_reading.py # Модель показаний датчиков
│   │   └── user.py         # Модель пользователей
│   └── service/
│       └── password_service.py # Сервис работы с паролями
├── scripts/
│   └── init_db.py          # Скрипт инициализации БД
└── main.py                 # Точка входа приложения
```

## 🚀 Быстрый старт

### Требования

- Python 3.9+
- pip
- virtualenv (рекомендуется)

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

## 🔧 Конфигурация

Создайте файл `.env` в корне проекта:

```env
PROJECT_NAME="My IoT Project"
DEBUG=True
DATABASE_URL="sqlite:///./test.db"
```

### Поддерживаемые параметры:

- `PROJECT_NAME` - Название проекта
- `DEBUG` - Режим отладки (True/False)
- `DATABASE_URL` - URL подключения к БД

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
# Запуск тестов (когда будут добавлены)
pytest tests/
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

## 🛠️ Разработка

### Структура кода

- **Models** (`app/models/`): SQLAlchemy модели для БД
- **API Routes** (`app/api/v1/`): Эндпоинты REST API
- **Enums** (`app/api/enums/`): Перечисления и константы
- **Services** (`app/service/`): Бизнес-логика
- **Core** (`app/core/`): Конфигурация и общие компоненты

### Добавление нового типа датчика

1. Обновите `app/api/enums/sensor_type.py`:
   ```python
   class SensorType(str, Enum):
       TEMPERATURE = "temperature"
       HUMIDITY = "humidity"
       PRESSURE = "pressure"  # Новый тип
   ```

2. Обработка показаний автоматически поддержит новый тип

### Добавление нового типа оповещения

1. Обновите `app/api/enums/alert_type.py`:
   ```python
   class AlertType(str, Enum):
       TEMPERATURE = "temperature"
       PRESSURE = "pressure"  # Новый тип
   ```

## 📈 Production Checklist

- [ ] Замените SQLite на PostgreSQL/MySQL
- [ ] Внедрите bcrypt/Argon2 для паролей
- [ ] Добавьте JWT authentication
- [ ] Настройте CORS
- [ ] Добавьте rate limiting
- [ ] Настройте логирование
- [ ] Добавьте мониторинг (Prometheus/Grafana)
- [ ] Настройте CI/CD
- [ ] Добавьте юнит-тесты
- [ ] Настройте Docker
- [ ] Добавьте документацию API
- [ ] Настройте резервное копирование БД

## 🐳 Docker

```dockerfile
# Dockerfile (пример)
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml (пример)
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/iot
    depends_on:
      - db
  
  db:
    image: postgres:14
    environment:
      POSTGRES_DB: iot
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

## 📄 Лицензия

[Укажите лицензию проекта]

## 👥 Авторы

[Информация об авторах проекта]

## 🤝 Вклад

Мы приветствуем вклад в проект! Пожалуйста:

1. Fork репозиторий
2. Создайте feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit изменения (`git commit -m 'Add some AmazingFeature'`)
4. Push в branch (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

## 📞 Поддержка

Если у вас возникли вопросы или проблемы:
- Создайте Issue в GitHub
- Напишите в [контакты проекта]

---

Made with ❤️ using FastAPI and Python
