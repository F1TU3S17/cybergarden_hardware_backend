"""Скрипт инициализации базы данных.

Этот скрипт создает все таблицы в базе данных на основе
определенных SQLAlchemy моделей.

Использование:
    # Windows PowerShell
    .\.\.venv\Scripts\Activate.ps1
    python scripts\init_db.py
    
    # Linux/Mac
    source .venv/bin/activate
    python scripts/init_db.py
    
Что делает скрипт:
    1. Загружает конфигурацию БД из app.core.config
    2. Создает все таблицы, если они еще не существуют:
       - users (пользователи)
       - devices (устройства)
       - sensor_readings (показания датчиков)
       - alerts (оповещения)
       - commands (команды)
       - logs (логи)
    3. Выводит сообщение об успешной инициализации

Примечание:
    Скрипт безопасен для многократного выполнения -
    он не перезаписывает существующие таблицы и данные.
"""

from app.db.session import init_db


if __name__ == "__main__":
    # Инициализация базы данных
    init_db()
    print("✅ Database initialized (tables created)")
    print("ℹ️ Таблицы успешно созданы или уже существуют")
    print("☎️ Для запуска сервера используйте: uvicorn main:app --reload --port 8000")
