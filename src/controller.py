from src.states import PetState


class PetController:

    def __init__(self, animation_player):

        self.animation = animation_player

        self.state = None

        self.set_state(PetState.IDLE)

    def set_state(self, new_state):

        if new_state == self.state:
            return

        self.state = new_state

        print(f"Pet state changed to: {self.state.name}")

        if new_state == PetState.IDLE:

            self.animation.play(
                "assets/cat/idle/Cat-2-Idle.png",
                frame_count=10,
                frame_duration=100,
            )

        elif new_state == PetState.WALK:

            self.animation.play(
                "assets/cat/walk/Cat-2-Walk.png",
                frame_count=8,
                frame_duration=100,
            )

        elif new_state == PetState.SIT:

            self.animation.play(
                "assets/cat/sitting/Cat-2-Sitting.png",
                frame_count=1,
                frame_duration=120,
            )
