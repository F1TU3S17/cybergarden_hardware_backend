"""Тестовый скрипт для проверки работы Redis."""

from app.db.redis_client import redis_client

def test_redis_connection():
    """Тест подключения к Redis."""
    print("Testing Redis connection...")
    
    # Тест подключения
    if redis_client.ping():
        print("✅ Redis connection successful!")
    else:
        print("❌ Redis connection failed!")
        return
    
    # Тест сохранения значений устройства
    test_device_id = "test-device-123"
    test_values = {
        "temperature_limit": 25.5,
        "humidity_limit": 60.0,
        "fire_limit": 100.0,
        "servo_position": 90
    }
    
    print(f"\n📝 Saving test values for device {test_device_id}...")
    success = redis_client.set_device_values(test_device_id, test_values)
    
    if success:
        print("✅ Values saved successfully!")
    else:
        print("❌ Failed to save values!")
        return
    
    # Тест чтения значений
    print(f"\n📖 Reading values for device {test_device_id}...")
    retrieved_values = redis_client.get_device_values(test_device_id)
    
    if retrieved_values:
        print("✅ Values retrieved successfully!")
        print(f"   Retrieved: {retrieved_values}")
        
        # Проверка соответствия
        if retrieved_values == test_values:
            print("✅ Values match!")
        else:
            print("❌ Values don't match!")
    else:
        print("❌ Failed to retrieve values!")
        return
    
    # Тест обновления одного поля
    print(f"\n🔄 Updating temperature_limit to 30.0...")
    success = redis_client.update_device_value(test_device_id, "temperature_limit", 30.0)
    
    if success:
        print("✅ Field updated successfully!")
        updated_values = redis_client.get_device_values(test_device_id)
        print(f"   New temperature_limit: {updated_values.get('temperature_limit')}")
    else:
        print("❌ Failed to update field!")
    
    # Тест получения всех устройств
    print(f"\n📋 Getting all devices with values...")
    all_devices = redis_client.get_all_devices_with_values()
    print(f"✅ Found {len(all_devices)} device(s) with values")
    for device_id, values in all_devices.items():
        print(f"   - {device_id}: {values}")
    
    # Очистка тестовых данных
    print(f"\n🗑️  Cleaning up test data...")
    success = redis_client.delete_device_values(test_device_id)
    
    if success:
        print("✅ Test data cleaned up!")
    else:
        print("❌ Failed to clean up test data!")
    
    print("\n✨ All tests completed!")

if __name__ == "__main__":
    test_redis_connection()
