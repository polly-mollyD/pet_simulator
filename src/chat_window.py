
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextBrowser,
    QLineEdit,
    QPushButton,
)
from src.ai_client import generate_reply

from PySide6.QtCore import QThread, Signal



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
        self.resize(300, 400)

        layout = QVBoxLayout(self)

        self.conversation = QTextBrowser()
        layout.addWidget(self.conversation)

        self.message_input = QLineEdit()
        self.message_input.setPlaceholderText("Ask your cat something...")
        layout.addWidget(self.message_input)

        self.send_button = QPushButton("Send")
        layout.addWidget(self.send_button)

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
        self.message_input.setEnabled(True)
        self.message_input.setFocus()


    def add_message(self, speaker, message):
        self.conversation.append(f"{speaker}:")
        self.conversation.insertPlainText("\n" + message + "\n")


    def wait_for_reply(self):
        if self.worker is not None:
            self.worker.wait()
