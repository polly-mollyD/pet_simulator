from PySide6.QtCore import Qt, QPoint, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMenu,
    QWidget,
    QSystemTrayIcon
)
from src.state_config import STATE_CONFIG
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
        self.state_timer.start(STATE_CONFIG[PetState.IDLE]["duration"])

        self.animation.animation_finished.connect(self.on_animation_finished)

        self.movement_timer = QTimer(self)
        self.movement_timer.timeout.connect(self.move_pet)
        self.movement_timer.start(30)


        self.tray_menu = QMenu(self)

        quit_action = self.tray_menu.addAction("Quit")
        quit_action.triggered.connect(QApplication.quit)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(self.pet_label.pixmap()))
        self.tray_icon.setToolTip("Desktop Pet")
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.show()

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


    def change_state(self, state):

        self.controller.set_state(state)

        self.resize(
            self.animation.display_width,
            self.animation.display_height,
        )

        duration = STATE_CONFIG[state]["duration"]

        if duration is None:
            self.state_timer.stop()
        else:
            self.state_timer.start(duration)


    def move_pet(self):
        if QApplication.mouseButtons() & Qt.LeftButton:
            return
        
        speed = STATE_CONFIG[self.controller.state].get("speed", 0)
        if speed == 0:
            return
        
        screen = self.screen().availableGeometry()
        left = screen.left()
        right = screen.right() + 1 - self.width()

        x = self.x() + speed * self.animation.direction

        if x <= left or x >= right:
            self.animation.direction *= -1
            self.animation.show_frame()

        self.move(max(left, min(x, right)), self.y())



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

        states = list(STATE_CONFIG)

        next_state = random.choice([
            state for state in states
            for _ in range(STATE_CONFIG[state]["probability"])
        ])
        self.change_state(next_state)
