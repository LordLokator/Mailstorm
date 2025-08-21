from enum import Enum


class Mode(Enum):
    FULL_CONVERSATION = "mail"
    AUTO_SPLIT = "chunk"
    MANUAL_SPLIT = "split"
