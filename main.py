import sys

from PySide6.QtCore import Qt, QPoint
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

        # Remove normal Windows frame and keep the pet above other windows.
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.Tool
        )

        # Make the window background transparent.
        self.setAttribute(Qt.WA_TranslucentBackground)

        # ----- Pet image -----
        self.pet_label = QLabel(self)

        path = "assets/kate.png"
        pixmap = QPixmap(path)

        if pixmap.isNull():
            raise FileNotFoundError(f"Could not load {path}")

        # Resize while preserving proportions.
        pixmap = pixmap.scaled(
            200,
            200,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )

        self.pet_label.setPixmap(pixmap)
        self.pet_label.resize(pixmap.size())

        # Make the actual window exactly the size of the pet.
        self.resize(pixmap.size())

        # Used when dragging the pet.
        self.drag_position = QPoint()

        # Start near the bottom-right corner.
        screen = QApplication.primaryScreen().availableGeometry()

        x = screen.right() - self.width() - 30
        y = screen.bottom() - self.height() - 30

        self.move(x, y)

    # -------------------------
    # Dragging
    # -------------------------

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

    # -------------------------
    # Right-click menu
    # -------------------------

    def contextMenuEvent(self, event):
        menu = QMenu(self)

        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(QApplication.quit)

        menu.addAction(quit_action)

        menu.exec(event.globalPos())


def main():
    app = QApplication(sys.argv)

    pet = PetWindow()
    pet.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()