# Redis Integration для Device Values

## Описание

Интеграция Redis для быстрого хранения и получения значений устройств (лимиты температуры, влажности, позиции сервоприводов и т.д.).

## Установка

Redis уже добавлен в `requirements.txt` и установлен.

## Настройка

Настройки Redis в `app/core/config.py`:

```python
REDIS_HOST: str = "localhost"
REDIS_PORT: int = 6379
REDIS_DB: int = 0
REDIS_PASSWORD: str | None = None
REDIS_DECODE_RESPONSES: bool = True
```

Можно переопределить через переменные окружения в `.env`:

```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=your_password_if_needed
```

## API Endpoints

### 1. Установить значения устройства (POST)

**Endpoint:** `POST /api/v1/devices/{device_id}/values`

**Body (JSON):**
```json
{
  "device_id": "550e8400-e29b-41d4-a716-446655440000",
  "temperature_limit": 25.5,
  "humidity_limit": 60.0,
  "fire_limit": 100.0,
  "servo_position": 90
}
```

**Response:**
```json
{
  "success": true,
  "device_id": "550e8400-e29b-41d4-a716-446655440000",
  "values": {
    "temperature_limit": 25.5,
    "humidity_limit": 60.0,
    "fire_limit": 100.0,
    "servo_position": 90
  },
  "message": "Device values successfully saved to Redis"
}
```

**Примечание:** Все поля опциональны. Можно передать только те значения, которые нужно обновить.

### 2. Получить значения устройства (GET)

**Endpoint:** `GET /api/v1/devices/{device_id}/values`

**Response:**
```json
{
  "device_id": "550e8400-e29b-41d4-a716-446655440000",
  "device_name": "Sensor_001",
  "values": {
    "temperature_limit": 25.5,
    "humidity_limit": 60.0,
    "fire_limit": 100.0,
    "servo_position": 90
  }
}
```

Если значений нет в Redis:
```json
{
  "device_id": "550e8400-e29b-41d4-a716-446655440000",
  "device_name": "Sensor_001",
  "values": {}
}
```

## Примеры использования

### Python (httpx)

```python
import httpx

# Установить значения
response = httpx.post(
    "http://localhost:8000/api/v1/devices/test-device-123/values",
    json={
        "device_id": "test-device-123",
        "temperature_limit": 25.5,
        "humidity_limit": 60.0
    }
)
print(response.json())

# Получить значения
response = httpx.get(
    "http://localhost:8000/api/v1/devices/test-device-123/values"
)
print(response.json())
```

### cURL

```bash
# Установить значения
curl -X POST "http://localhost:8000/api/v1/devices/test-device-123/values" \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "test-device-123",
    "temperature_limit": 25.5,
    "humidity_limit": 60.0,
    "fire_limit": 100.0,
    "servo_position": 90
  }'

# Получить значения
curl "http://localhost:8000/api/v1/devices/test-device-123/values"
```

### JavaScript (fetch)

```javascript
// Установить значения
const response = await fetch('http://localhost:8000/api/v1/devices/test-device-123/values', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    device_id: 'test-device-123',
    temperature_limit: 25.5,
    humidity_limit: 60.0,
    fire_limit: 100.0,
    servo_position: 90
  })
});
const data = await response.json();
console.log(data);

// Получить значения
const getResponse = await fetch('http://localhost:8000/api/v1/devices/test-device-123/values');
const values = await getResponse.json();
console.log(values);
```

## Структура хранения в Redis

Ключи хранятся в формате:
```
device:values:{device_id}
```

Значения хранятся как JSON строки:
```json
{
  "temperature_limit": 25.5,
  "humidity_limit": 60.0,
  "fire_limit": 100.0,
  "servo_position": 90
}
```

## Использование RedisClient напрямую

Если нужно работать с Redis вне API endpoints:

```python
from app.db.redis_client import redis_client

# Проверка подключения
if redis_client.ping():
    print("Redis connected!")

# Сохранить значения
redis_client.set_device_values("device-123", {
    "temperature_limit": 25.5,
    "humidity_limit": 60.0
})

# Получить значения
values = redis_client.get_device_values("device-123")
print(values)

# Обновить одно поле
redis_client.update_device_value("device-123", "temperature_limit", 30.0)

# Получить все устройства с values
all_devices = redis_client.get_all_devices_with_values()

# Удалить значения
redis_client.delete_device_values("device-123")
```

## Тестирование

Запустите тестовый скрипт:

```bash
python test_redis.py
```

## Преимущества использования Redis

1. **Быстрый доступ**: Redis хранит данные в памяти, обеспечивая мгновенный доступ
2. **Легкий для IoT устройств**: Устройства могут быстро получать свои настройки
3. **Масштабируемость**: Redis легко масштабируется для тысяч устройств
4. **TTL поддержка**: Можно установить время жизни для значений (опционально)
5. **Атомарные операции**: Безопасное обновление значений в многопоточной среде

## Возможные улучшения

1. Добавить TTL (время жизни) для автоматического удаления старых значений
2. Использовать Redis Pub/Sub для real-time уведомлений об изменениях
3. Добавить кэширование других данных (последние показания, статусы и т.д.)
4. Использовать Redis Streams для логирования изменений
