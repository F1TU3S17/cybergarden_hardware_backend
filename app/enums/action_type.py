from enum import Enum
class ActionType(str, Enum):
    TOGGLE_ALERT = 'toggle_alert'
    TOGGLE_SERVO = 'toggle_servo'
    SET_SERVO_POSITION = 'set_servo_position'
    SET_TEMPERATURE_LIMIT = 'set_temerature_limit'
    SET_FIRE_LIMIT = 'set_fire_limit'
    SET_HUMIDITY_LIMIT = 'set_humidity_limit'


