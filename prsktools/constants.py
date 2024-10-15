from enum import IntEnum, auto


class Difficulty(IntEnum):
    Easy = auto()
    Normal = auto()
    Hard = auto()
    Expert = auto()
    Master = auto()
    Append = auto()


class Status(IntEnum):
    Default = auto()
    Clear = auto()
    FC = auto()
    AP = auto()
