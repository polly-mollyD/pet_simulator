from enum import Enum, auto


class PetState(Enum):
    IDLE = auto()
    WALK = auto()
    SIT = auto()
    SLEEP = auto()
    LAY = auto()
    STRETCH = auto()
    LICK = auto()
    ITCH = auto()
    MEOW = auto()
    RUN = auto()