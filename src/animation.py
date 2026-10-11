from pathlib import Path

from PySide6.QtCore import QObject, QTimer, Qt, Signal
from PySide6.QtGui import QPixmap, QTransform, QPainter

class AnimationPlayer(QObject):
    animation_finished = Signal()

    def __init__(self, label, scale=3):
        super().__init__()

        self.label = label
        self.scale = scale
        self.direction = 1

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
        loop=True,
        reverse=False,
        effect_path=None,
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

        self.loop = loop
        self.frame_count = frame_count
        self.current_frame = 0
        self.reverse = reverse

        self.frame_width = (
            self.sprite_sheet.width() // frame_count
        )

        self.frame_height = self.sprite_sheet.height()

        self.label.resize(
            self.frame_width * self.scale,
            self.frame_height * self.scale,
        )
        self.effect_sheet = QPixmap(effect_path) if effect_path else None

        self.show_frame()

        self.timer.start(frame_duration)


    def show_frame(self):

        x = self.current_frame * self.frame_width

        if self.reverse:
            x = (self.frame_count - 1 - self.current_frame) * self.frame_width

        frame = self.sprite_sheet.copy(
            x,
            0,
            self.frame_width,
            self.frame_height,
        )

        if self.effect_sheet is not None and self.current_frame > 0:
            effect_index = (self.current_frame - 1) % 3
            effect = self.effect_sheet.copy(effect_index * 16, 0, 16, 16)

            painter = QPainter(frame)
            painter.drawPixmap(34, 18, effect)
            painter.end()

        frame = frame.scaled(
            self.frame_width * self.scale,
            self.frame_height * self.scale,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )

        if self.direction == -1:
            frame = frame.transformed(QTransform().scale(-1, 1))
        self.label.setPixmap(frame)


    def next_frame(self):
        if self.current_frame == self.frame_count - 1:
            if self.loop:
                self.current_frame = 0
            else:
                self.timer.stop()
                self.animation_finished.emit()
                return
        else:
            self.current_frame += 1

        self.show_frame()


    @property
    def display_width(self):
        return self.frame_width * self.scale

    @property
    def display_height(self):
        return self.frame_height * self.scale
