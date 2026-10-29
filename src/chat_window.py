
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextBrowser,
    QLineEdit,
    QPushButton,
    QLabel,
    QHBoxLayout
)
from src.ai_client import generate_reply

from PySide6.QtCore import QThread, Signal

from PySide6.QtGui import (
    QColor, QTextBlockFormat, QTextCharFormat, QTextCursor
)


class ReplyWorker(QThread):
    reply_ready = Signal(str)
    reply_failed = Signal(str)

    def __init__(self, messages, parent=None):
        super().__init__(parent)
        self.messages = [message.copy() for message in messages]

    def run(self):
        try:
            reply = generate_reply(self.messages)
        except Exception as error:
            self.reply_failed.emit(str(error))
        else:
            self.reply_ready.emit(reply)


class ChatWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.worker = None

        self.setWindowTitle("Chat with your cat")
        self.resize(420, 520)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Heading at the top
        title = QLabel("Chat with your cat")
        title.setObjectName("chatTitle")
        layout.addWidget(title)

        # Conversation in the middle
        self.conversation = QTextBrowser()
        layout.addWidget(self.conversation, 1)

        # Message input and button at the bottom
        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText(
            "Ask your cat something..."
        )

        self.send_button = QPushButton("Send")

        input_layout = QHBoxLayout()
        input_layout.setSpacing(8)
        input_layout.addWidget(self.message_input, 1)
        input_layout.addWidget(self.send_button)

        layout.addLayout(input_layout)


        self.send_button.clicked.connect(self.send_message)
        self.message_input.returnPressed.connect(self.send_message)

        self.messages = [
            {
                "role": "system",
                "content": (
                    "You are a friendly desktop cat companion. "
                    "Give helpful, concise answers with a playful personality."
                ),
            }
        ]

        self.setStyleSheet("""
            QWidget {
                background-color: #181825;
                color: #cdd6f4;
                font-family: "Segoe UI";
                font-size: 14px;
            }

            QLabel#chatTitle {
                font-size: 20px;
                font-weight: bold;
                padding-bottom: 4px;
            }

            QTextBrowser {
                background-color: #1e1e2e;
                border: 1px solid #45475a;
                border-radius: 12px;
                padding: 12px;
            }

            QLineEdit {
                background-color: #313244;
                border: 1px solid #45475a;
                border-radius: 10px;
                padding: 10px;
                selection-background-color: #585b70;
            }

            QLineEdit:focus {
                border: 1px solid #cba6f7;
            }

            QPushButton {
                background-color: #cba6f7;
                color: #181825;
                border: none;
                border-radius: 10px;
                padding: 10px 16px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #b4befe;
            }

            QPushButton:disabled {
                background-color: #45475a;
                color: #a6adc8;
            }
        """)


    def send_message(self):
        if self.worker is not None:
            return

        message = self.message_input.text().strip()

        if not message:
            return

        self.add_message("You", message)
        self.message_input.clear()

        self.send_button.setEnabled(False)
        self.message_input.setEnabled(False)
        self.send_button.setText("Thinking…")

        self.messages.append({
            "role": "user",
            "content": message,
        })
        self.worker = ReplyWorker(self.messages, self)

        self.worker.reply_ready.connect(self.receive_reply)
        self.worker.reply_failed.connect(self.receive_error)
        self.worker.finished.connect(self.finish_reply)

        self.worker.start()


    def receive_reply(self, reply):
        self.messages.append({
            "role": "assistant",
            "content": reply,
        })
        self.add_message("Cat", reply)


    def receive_error(self, error):
        failed_message = self.messages.pop()

        self.add_message("Error", error)
        self.message_input.setText(failed_message["content"])


    def finish_reply(self):
        self.worker.deleteLater()
        self.worker = None

        self.send_button.setEnabled(True)
        self.send_button.setText("Send")
        self.message_input.setEnabled(True)
        self.message_input.setFocus()


    def add_message(self, speaker, message):
        cursor = self.conversation.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)

        background = QTextBlockFormat()
        background.setBackground(
            QColor("#45405a" if speaker == "You" else "#1e1e2e")
        )

        if not self.conversation.document().isEmpty():
            cursor.insertBlock()

        cursor.setBlockFormat(background)
        cursor.setCharFormat(QTextCharFormat())
        cursor.insertText(f"{speaker}:\n{message}")

        self.conversation.setTextCursor(cursor)
        self.conversation.ensureCursorVisible()


    def wait_for_reply(self):
        if self.worker is not None:
            self.worker.wait()
