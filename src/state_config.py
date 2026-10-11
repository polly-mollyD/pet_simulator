from src.states import PetState

STATE_CONFIG = {
    PetState.IDLE:    {"duration": 2000,  "probability": 5},
    PetState.WALK:    {"duration": 8000,  "probability": 35, "speed": 2},
    PetState.RUN:     {"duration": 4000,  "probability": 10, "speed": 4},
    PetState.SIT:     {"duration": 4000,  "probability": 10},
    PetState.LAY:     {"duration": None,  "probability": 15},
    PetState.SLEEP1:  {"duration": 15000, "probability": 0},
    PetState.SLEEP2:  {"duration": 15000, "probability": 0},
    PetState.WAKE_UP: {"duration": None,  "probability": 0},
    PetState.STRETCH: {"duration": None,  "probability": 5},
    PetState.MEOW:    {"duration": 1000,  "probability": 5},
    PetState.ITCH:    {"duration": 2000,  "probability": 5},
    PetState.LICK1:   {"duration": 3000,  "probability": 5},
    PetState.LICK2:   {"duration": 3000,  "probability": 5},
}