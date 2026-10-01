import sys

from PySide6.QtCore import Qt, QPoint, QTimer
from PySide6.QtGui import QPixmap, QAction
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMenu,
    QWidget,
)


class PetWindow(QWidget):
    def __init__(self):
        super().__init__()

        # -------------------------
        # Window setup
        # -------------------------

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )

        self.setAttribute(Qt.WA_TranslucentBackground)

        # -------------------------
        # Load idle sprite sheet
        # -------------------------

        self.sprite_sheet = QPixmap(
            "assets/cat/idle/Cat-2-Idle.png"
        )

        if self.sprite_sheet.isNull():
            raise FileNotFoundError(
                "Could not load idle sprite sheet."
            )

        self.frame_count = 10

        self.frame_width = (
            self.sprite_sheet.width() // self.frame_count
        )

        self.frame_height = self.sprite_sheet.height()

        print("Sprite sheet size:",
              self.sprite_sheet.width(),
              "x",
              self.sprite_sheet.height())

        print("Individual frame size:",
              self.frame_width,
              "x",
              self.frame_height)

        # -------------------------
        # Pet label
        # -------------------------

        self.pet_label = QLabel(self)

        self.current_frame = 0

        # Scale factor
        self.display_scale = 3

        self.display_width = (
            self.frame_width * self.display_scale
        )

        self.display_height = (
            self.frame_height * self.display_scale
        )

        self.pet_label.resize(
            self.display_width,
            self.display_height
        )

        self.resize(
            self.display_width,
            self.display_height
        )

        # -------------------------
        # Animation timer
        # -------------------------

        self.animation_timer = QTimer(self)

        self.animation_timer.timeout.connect(
            self.next_frame
        )

        # 100 ms = 10 FPS
        self.animation_timer.start(100)

        # Draw first frame
        self.show_frame()

        # -------------------------
        # Dragging
        # -------------------------

        self.drag_position = QPoint()

        # -------------------------
        # Starting position
        # -------------------------

        screen = QApplication.primaryScreen().availableGeometry()

        x = screen.right() - self.width() - 30
        y = screen.bottom() - self.height() - 30

        self.move(x, y)

    # =========================
    # ANIMATION
    # =========================

    def show_frame(self):

        x = self.current_frame * self.frame_width

        frame = self.sprite_sheet.copy(
            x,
            0,
            self.frame_width,
            self.frame_height
        )

        frame = frame.scaled(
            self.display_width,
            self.display_height,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.pet_label.setPixmap(frame)

    def next_frame(self):

        self.current_frame += 1

        if self.current_frame >= self.frame_count:
            self.current_frame = 0

        self.show_frame()

    # =========================
    # DRAGGING
    # =========================

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:

            self.drag_position = (
                event.globalPosition().toPoint()
                - self.frameGeometry().topLeft()
            )

            event.accept()

    def mouseMoveEvent(self, event):

        if event.buttons() & Qt.LeftButton:

            self.move(
                event.globalPosition().toPoint()
                - self.drag_position
            )

            event.accept()

    # =========================
    # RIGHT CLICK MENU
    # =========================

    def contextMenuEvent(self, event):

        menu = QMenu(self)

        quit_action = QAction("Quit", self)

        quit_action.triggered.connect(
            QApplication.quit
        )

        menu.addAction(quit_action)

        menu.exec(event.globalPos())


def main():

    app = QApplication(sys.argv)

    pet = PetWindow()

    pet.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()