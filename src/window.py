from PySide6.QtCore import Qt, QPoint, QTimer
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMenu,
    QWidget,
)

from src.animation import AnimationPlayer
from src.controller import PetController
from src.states import PetState
import random


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

        self.setAttribute(
            Qt.WA_TranslucentBackground
        )

        # -------------------------
        # Pet image
        # -------------------------

        self.pet_label = QLabel(self)

        # -------------------------
        # Animation system
        # -------------------------

        self.animation = AnimationPlayer(
            self.pet_label,
            scale=3,
        )

        # -------------------------
        # Pet controller
        # -------------------------

        self.controller = PetController(
            self.animation
        )

        # Resize the transparent window
        # to match the animation.
        self.resize(
            self.animation.display_width,
            self.animation.display_height,
        )

        # -------------------------
        # Dragging
        # -------------------------

        self.drag_position = QPoint()

        # -------------------------
        # Starting position
        # -------------------------

        screen = (
            QApplication
            .primaryScreen()
            .availableGeometry()
        )

        x = screen.right() - self.width() - 30
        y = screen.bottom() - self.height() - 30

        self.move(x, y)

        self.state_timer = QTimer(self)
        self.state_timer.timeout.connect(self.choose_random_state)
        self.state_timer.start(5000)

        self.animation.animation_finished.connect(self.on_animation_finished)

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

        idle_action = QAction("Idle", self)
        walk_action = QAction("Walk", self)
        sit_action = QAction("Sit", self)

        quit_action = QAction("Quit", self)

        idle_action.triggered.connect(
            lambda: self.change_state(
                PetState.IDLE
            )
        )

        walk_action.triggered.connect(
            lambda: self.change_state(
                PetState.WALK
            )
        )

        sit_action.triggered.connect(
            lambda: self.change_state(
                PetState.SIT
            )
        )

        quit_action.triggered.connect(
            QApplication.quit
        )

        menu.addAction(idle_action)
        menu.addAction(walk_action)
        menu.addAction(sit_action)

        menu.addSeparator()

        menu.addAction(quit_action)

        menu.exec(event.globalPos())


    def change_state(self, state):

        self.controller.set_state(state)

        self.resize(
            self.animation.display_width,
            self.animation.display_height,
        )

        if state in (PetState.LAY, PetState.WAKE_UP):
            self.state_timer.stop()
        elif state in (PetState.SLEEP1, PetState.SLEEP2):
            self.state_timer.start(15000)
        else:
            self.state_timer.start(5000)


    def on_animation_finished(self):
        if self.controller.state == PetState.LAY:
            sleep_state = random.choice([
                PetState.SLEEP1,
                PetState.SLEEP2,
            ])
            self.change_state(sleep_state)

        elif self.controller.state in (PetState.WAKE_UP, PetState.STRETCH):
            self.change_state(PetState.IDLE)


    def choose_random_state(self):
        if self.controller.state in (PetState.SLEEP1, PetState.SLEEP2):
            self.change_state(PetState.WAKE_UP)
            return

        states = [
            PetState.IDLE,
            PetState.WALK,
            PetState.SIT,
            PetState.LAY,
            PetState.ITCH,
            PetState.STRETCH,
            PetState.MEOW,
            PetState.RUN,
            PetState.LICK1,
            PetState.LICK2,
        ]

        next_state = random.choice(states)
        self.change_state(next_state)