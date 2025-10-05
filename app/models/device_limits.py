from pydantic import BaseModel

class DeviceValues(BaseModel):
    device_id: str
    temperature_limit: float
    humidity_limit: float
    fire_limit: float
    servo_position: int