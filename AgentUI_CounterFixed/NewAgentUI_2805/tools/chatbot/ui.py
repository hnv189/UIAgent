import sys
import threading
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QPushButton,
    QVBoxLayout, QWidget
)
from PyQt5.QtGui import QKeySequence, QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QTimer, QObject, pyqtSignal
from tools.chatbot.openai_client import OpenAIClient


class ChatInput(QTextEdit):
    def __init__(self, parent=None, send_callback=None):
        super().__init__(parent)
        self.send_callback = send_callback

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter) and not (event.modifiers() & Qt.ShiftModifier):
            if self.send_callback:
                self.send_callback()
            event.accept()
        else:
            super().keyPressEvent(event)


class WorkerSignals(QObject):
    finished = pyqtSignal(str)


class ChatBotUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chatbot")
        self.setGeometry(100, 100, 500, 400)

        self.openai_client = OpenAIClient()
        self.signals = WorkerSignals()

        self.initUI()
        self.apply_dark_theme()

        # For typing animation
        self.typing_timer = QTimer()
        self.typing_timer.timeout.connect(self.animate_typing)
        self.dot_count = 0
        self.typing_index = None

        self.signals.finished.connect(self.handle_bot_response)

    def initUI(self):
        layout = QVBoxLayout()

        self.chat_box = QTextEdit(self)
        self.chat_box.setReadOnly(True)
        self.chat_box.setFont(QFont("Arial", 12))
        layout.addWidget(self.chat_box)

        self.user_input = ChatInput(self, send_callback=self.send_message)
        self.user_input.setFont(QFont("Arial", 12))
        self.user_input.setFixedHeight(60)
        layout.addWidget(self.user_input)

        self.send_button = QPushButton("Send", self)
        self.send_button.setFont(QFont("Arial", 11))
        self.send_button.clicked.connect(self.send_message)
        layout.addWidget(self.send_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def send_message(self):
        user_message = self.user_input.toPlainText().strip()
        if not user_message:
            return

        self.chat_box.append(f"<b>You:</b> {user_message}")
        self.user_input.clear()
        QApplication.processEvents()

        # Add placeholder for typing animation
        self.chat_box.append("<b>Bot is typing</b>")
        self.typing_index = self.chat_box.document().blockCount() - 1
        self.dot_count = 0
        self.typing_timer.start(400)

        # Run in thread
        thread = threading.Thread(target=self.fetch_response, args=(user_message,))
        thread.start()

    def animate_typing(self):
        if self.typing_index is not None:
            cursor = self.chat_box.textCursor()
            block = self.chat_box.document().findBlockByNumber(self.typing_index)
            cursor.setPosition(block.position())
            cursor.select(cursor.LineUnderCursor)
            self.dot_count = (self.dot_count + 1) % 4
            dots = '.' * self.dot_count
            cursor.removeSelectedText()
            cursor.insertText(f"Bot is typing{dots}")

    def fetch_response(self, user_message):
        try:
            response = self.openai_client.send_message(user_message)
        except Exception as e:
            response = f"[Error: {str(e)}]"
        self.signals.finished.emit(response)

    def handle_bot_response(self, response):
        self.typing_timer.stop()
        self.typing_index = None
        self.chat_box.append(f"<b>Bot:</b> {response}")

    def apply_dark_theme(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(20, 20, 20))
        dark_palette.setColor(QPalette.AlternateBase, QColor(30, 30, 30))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(45, 45, 45))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.Highlight, QColor(100, 100, 255))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        QApplication.setPalette(dark_palette)

