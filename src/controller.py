from src.states import PetState
from src.state_config import STATE_CONFIG


class PetController:

    def __init__(self, animation_player):
        self.animation = animation_player
        self.state = None
        self.set_state(PetState.IDLE)

    def set_state(self, new_state):
        if new_state == self.state:
            return

        self.animation.play(**STATE_CONFIG[new_state]["animation"])
        self.state = new_state

        print(f"Pet state changed to: {self.state.name}")
