from enum import Enum, auto


class PetState(Enum):
    IDLE = auto()
    WALK = auto()
    SIT = auto()
    SLEEP1 = auto()
    SLEEP2 = auto()
    LAY = auto()
    STRETCH = auto()
    LICK1 = auto()
    LICK2 = auto()
    ITCH = auto()
    MEOW = auto()
    RUN = auto()
    WAKE_UP = auto()