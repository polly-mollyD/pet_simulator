from src.states import PetState

STATE_CONFIG = {
    PetState.IDLE: {
        "duration": 2000, "probability": 5,
        "animation": {
            "sprite_path": "assets/cat/idle/Cat-2-Idle.png",
            "frame_count": 10,
            "frame_duration": 100,
        },
    },
    PetState.WALK: {
        "duration": 8000, "probability": 35, "speed": 2,
        "animation": {
            "sprite_path": "assets/cat/walk/Cat-2-Walk.png",
            "frame_count": 8,
            "frame_duration": 100,
        },
    },
    PetState.RUN: {
        "duration": 4000, "probability": 10, "speed": 4,
        "animation": {
            "sprite_path": "assets/cat/run/Cat-2-Run.png",
            "frame_count": 8,
            "frame_duration": 120,
        },
    },
    PetState.SIT: {
        "duration": 4000, "probability": 10,
        "animation": {
            "sprite_path": "assets/cat/sitting/Cat-2-Sitting.png",
            "frame_count": 1,
            "frame_duration": 120,
        },
    },
    PetState.LAY: {
        "duration": None, "probability": 15,
        "animation": {
            "sprite_path": "assets/cat/laying/Cat-2-Laying.png",
            "frame_count": 8,
            "frame_duration": 120,
            "loop": False,
        },
    },
    PetState.SLEEP1: {
        "duration": 15000, "probability": 0,
        "animation": {
            "sprite_path": "assets/cat/sleeping1/Cat-2-Sleeping1.png",
            "frame_count": 1,
            "frame_duration": 120,
        },
    },
    PetState.SLEEP2: {
        "duration": 15000, "probability": 0,
        "animation": {
            "sprite_path": "assets/cat/sleeping2/Cat-2-Sleeping2.png",
            "frame_count": 1,
            "frame_duration": 120,
        },
    },
    PetState.WAKE_UP: {
        "duration": None, "probability": 0,
        "animation": {
            "sprite_path": "assets/cat/laying/Cat-2-Laying.png",
            "frame_count": 8,
            "frame_duration": 120,
            "loop": False,
            "reverse": True,
        },
    },
    PetState.STRETCH: {
        "duration": None, "probability": 5,
        "animation": {
            "sprite_path": "assets/cat/stretching/Cat-2-Stretching.png",
            "frame_count": 13,
            "frame_duration": 120,
            "loop": False,
        },
    },
    PetState.MEOW: {
        "duration": 1000, "probability": 5,
        "animation": {
            "sprite_path": "assets/cat/meow/Cat-2-Meow.png",
            "frame_count": 4,
            "frame_duration": 120,
            "effect_path": "assets/cat/meow/Meow-VFX.png",
        },
    },
    PetState.ITCH: {
        "duration": 2000, "probability": 5,
        "animation": {
            "sprite_path": "assets/cat/itch/Cat-2-Itch.png",
            "frame_count": 2,
            "frame_duration": 120,
        },
    },
    PetState.LICK1: {
        "duration": 3000, "probability": 5,
        "animation": {
            "sprite_path": "assets/cat/licking1/Cat-2-Licking 1.png",
            "frame_count": 5,
            "frame_duration": 120,
        },
    },
    PetState.LICK2: {
        "duration": 3000, "probability": 5,
        "animation": {
            "sprite_path": "assets/cat/licking2/Cat-2-Licking 2.png",
            "frame_count": 5,
            "frame_duration": 120,
        },
    },
}