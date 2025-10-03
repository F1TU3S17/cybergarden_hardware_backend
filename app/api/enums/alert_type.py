from enum import Enum


class AlertType(str, Enum):
    STUDY = "study"
    ERROR = "error"
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    MOTION = "motion"
    BATTERY = "battery"
    