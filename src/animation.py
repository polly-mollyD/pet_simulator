from pathlib import Path

from PySide6.QtCore import QObject, QTimer, Qt
from PySide6.QtGui import QPixmap

class AnimationPlayer(QObject):

    def __init__(self, label, scale=3):
        super().__init__()

        self.label = label
        self.scale = scale

        self.sprite_sheet = None

        self.frame_count = 0
        self.current_frame = 0

        self.frame_width = 0
        self.frame_height = 0

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_frame)

    def play(
        self,
        sprite_path,
        frame_count,
        frame_duration=100,
    ):
        """
        Start playing a sprite-sheet animation.

        sprite_path:
            Path to the sprite sheet.

        frame_count:
            Number of frames in the sheet.

        frame_duration:
            Time each frame is displayed in milliseconds.
        """

        sprite_path = Path(sprite_path)

        self.sprite_sheet = QPixmap(str(sprite_path))

        if self.sprite_sheet.isNull():
            raise FileNotFoundError(
                f"Could not load sprite sheet: {sprite_path}"
            )

        self.frame_count = frame_count
        self.current_frame = 0

        self.frame_width = (
            self.sprite_sheet.width() // frame_count
        )

        self.frame_height = self.sprite_sheet.height()

        self.label.resize(
            self.frame_width * self.scale,
            self.frame_height * self.scale,
        )

        self.show_frame()

        self.timer.start(frame_duration)


    def show_frame(self):

        x = self.current_frame * self.frame_width

        frame = self.sprite_sheet.copy(
            x,
            0,
            self.frame_width,
            self.frame_height,
        )

        frame = frame.scaled(
            self.frame_width * self.scale,
            self.frame_height * self.scale,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )

        self.label.setPixmap(frame)

    def next_frame(self):

        self.current_frame += 1

        if self.current_frame >= self.frame_count:
            self.current_frame = 0

        self.show_frame()


    @property
    def display_width(self):
        return self.frame_width * self.scale

    @property
    def display_height(self):
        return self.frame_height * self.scale