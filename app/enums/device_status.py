from enum import Enum


class DeviceStatus(str, Enum):
    ACTIVE = "online"
    OFFLINE = "offline"