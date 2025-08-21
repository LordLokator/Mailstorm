from enum import Enum, auto


class Mode(Enum):
    FULL_CONVERSATION = auto()
    AUTO_SPLIT = auto()
    MANUAL_SPLIT = auto()
