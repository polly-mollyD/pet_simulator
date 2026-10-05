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
                loop=True,
            )

        elif new_state == PetState.WALK:

            self.animation.play(
                "assets/cat/walk/Cat-2-Walk.png",
                frame_count=8,
                frame_duration=100,
                loop=True,
            )

        elif new_state == PetState.SIT:

            self.animation.play(
                "assets/cat/sitting/Cat-2-Sitting.png",
                frame_count=1,
                frame_duration=120,
                loop=True,
            )

        elif new_state == PetState.SLEEP1:

            self.animation.play(
                "assets/cat/sleeping1/Cat-2-Sleeping1.png",
                frame_count=1,
                frame_duration=120,
                loop=True,
            )

        elif new_state == PetState.SLEEP2:

            self.animation.play(
                "assets/cat/sleeping2/Cat-2-Sleeping2.png",
                frame_count=1,
                frame_duration=120,
                loop=True,
            )       

        elif new_state == PetState.STRETCH:

            self.animation.play(
                "assets/cat/stretching/Cat-2-Stretching.png",
                frame_count=13,
                frame_duration=120,
                loop=False,
            )

        elif new_state == PetState.RUN:

            self.animation.play(
                "assets/cat/run/Cat-2-Run.png",
                frame_count=8,
                frame_duration=120,
                loop=True,
            )

        elif new_state == PetState.MEOW:

            self.animation.play(
                "assets/cat/meow/Cat-2-Meow.png",
                frame_count=4,
                frame_duration=120,
                loop=True,
            )

        elif new_state == PetState.LICK1:

            self.animation.play(
                "assets/cat/licking1/Cat-2-Licking 1.png",
                frame_count=5,
                frame_duration=120,
                loop=True,
            )

        elif new_state == PetState.LICK2:

            self.animation.play(
                "assets/cat/licking2/Cat-2-Licking 2.png",
                frame_count=5,
                frame_duration=120,
                loop=True,
            )

        elif new_state == PetState.LAY:

            self.animation.play(
                "assets/cat/laying/Cat-2-Laying.png",
                frame_count=8,
                frame_duration=120,
                loop=False,
            )

        elif new_state == PetState.ITCH:

            self.animation.play(
                "assets/cat/itch/Cat-2-Itch.png",
                frame_count=2,
                frame_duration=120,
                loop=True,
            )

        elif new_state == PetState.WAKE_UP:
            
            self.animation.play(
                "assets/cat/laying/Cat-2-Laying.png",
                frame_count=8,
                frame_duration=120,
                loop=False,
                reverse=True,
            )