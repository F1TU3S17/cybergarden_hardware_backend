from enum import Enum

class CommandStatus(str, Enum):
    PENDING = "pending"
    FINISHED = "finished"
    REJECTED = "rejected"