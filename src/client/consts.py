from enum import Enum

class TrainServiceState(Enum):
    ON_TIME = "On Time"
    DELAYED = "Delayed"
    DELAYED_NO_ETD = "Delayed with no estimate"
    CANCELLED = "Cancelled"