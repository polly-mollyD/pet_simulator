from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextBrowser,
    QLineEdit,
    QPushButton,
)
import time

from PySide6.QtCore import QThread, Signal



class ReplyWorker(QThread):
    reply_ready = Signal(str)

    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.message = message

    def run(self):
        time.sleep(3)

        reply = f'Meow! You said: "{self.message}"'
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

        self.worker = ReplyWorker(message, self)

        self.worker.reply_ready.connect(self.receive_reply)
        self.worker.finished.connect(self.finish_reply)

        self.worker.start()


    def receive_reply(self, reply):
        self.add_message("Cat", reply)


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