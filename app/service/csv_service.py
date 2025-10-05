"""CSV Service для экспорта данных в формат CSV.

Этот модуль предоставляет функциональность для экспорта данных
из различных моделей в формат CSV.

Functions:
    export_sensor_readings_to_csv: Экспорт показаний датчиков в CSV
"""

import csv
from io import StringIO
from typing import List
from app.models.sensor_reading import SensorReading


def export_sensor_readings_to_csv(readings: List[SensorReading]) -> str:
    """Экспортирует список показаний датчиков в CSV формат.
    
    Создает CSV-строку с данными показаний датчиков, включая заголовки.
    Формат включает: ID, Device ID, Sensor Type, Value, Unit, Timestamp.
    
    Args:
        readings (List[SensorReading]): Список показаний датчиков для экспорта
        
    Returns:
        str: CSV-строка с данными показаний датчиков
        
    Example:
        >>> readings = db.query(SensorReading).filter(
        ...     SensorReading.device_id == "device_123"
        ... ).all()
        >>> csv_data = export_sensor_readings_to_csv(readings)
        >>> print(csv_data)
        id,device_id,sensor_type,value,unit,timestamp
        abc-123,device_123,temperature,23.5,°C,2024-01-15 10:30:00
        
    Note:
        CSV использует запятую в качестве разделителя.
        Даты форматируются в ISO формат (YYYY-MM-DD HH:MM:SS).
    """
    # Создаем буфер для записи CSV
    output = StringIO()
    
    # Определяем заголовки CSV
    fieldnames = [
        'id',
        'device_id',
        'sensor_type',
        'value',
        'unit',
        'timestamp'
    ]
    
    # Создаем CSV writer
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    
    # Записываем заголовки
    writer.writeheader()
    
    # Записываем данные
    for reading in readings:
        writer.writerow({
            'id': reading.id,
            'device_id': reading.device_id,
            'sensor_type': reading.sensor_type,
            'value': reading.value,
            'unit': reading.unit or '',  # Используем пустую строку если unit == None
            'timestamp': reading.timestamp.strftime('%Y-%m-%d %H:%M:%S') if reading.timestamp else ''
        })
    
    # Получаем CSV как строку
    csv_content = output.getvalue()
    output.close()
    
    return csv_content
