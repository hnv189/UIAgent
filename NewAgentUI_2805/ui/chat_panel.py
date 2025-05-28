from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLineEdit
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class ChatPanel(QWidget):
    """Chat interface panel"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.chat_widgets = []
        self.chatbox_minimized = True
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Minimize/Expand button
        minimize_btn = QPushButton("−")
        minimize_btn.setFixedWidth(30)
        minimize_btn.setStyleSheet("""
            QPushButton {
                background: #e3e6e8;
                color: #222;
                border-radius: 6px;
                font-weight: bold;
                font-size: 16pt;
            }
            QPushButton:hover {
                background: #b2ebf2;
            }
        """)
        minimize_btn.clicked.connect(self.toggle_chatbox)

        chat_header = QHBoxLayout()
        chat_header.addStretch()
        chat_header.addWidget(minimize_btn)
        layout.addLayout(chat_header)

        # Chat display area
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setFixedHeight(80)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background: #f7f9fa;
                color: #222;
                border: 1px solid #4fc3f7;
                border-radius: 6px;
                font-size: 11pt;
            }
        """)
        layout.addWidget(self.chat_display)
        
        # Input area with text field and send button
        input_row = QHBoxLayout()
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("What would you like to do today? Choose a mode or a tool to get started.")
        self.chat_input.setMinimumHeight(36)
        self.chat_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #4fc3f7;
                border-radius: 6px;
                padding: 6px 12px;
                background: #fff;
                color: #222;
                font-size: 11pt;
            }
        """)
        
        send_btn = QPushButton("Send")
        send_btn.setMinimumHeight(36)
        send_btn.setStyleSheet("""
            QPushButton {
                background: #4fc3f7;
                color: #fff;
                border-radius: 6px;
                font-weight: bold;
                padding: 0 24px;
            }
            QPushButton:hover {
                background: #039be5;
            }
        """)
        send_btn.clicked.connect(self.send_chat_message)
        self.chat_input.returnPressed.connect(lambda: send_btn.click())

        input_row.addWidget(self.chat_input)
        input_row.addWidget(send_btn)
        layout.addLayout(input_row)

        # Add widgets to list for visibility toggling
        self.chat_widgets = [self.chat_display, self.chat_input, send_btn]
        for widget in self.chat_widgets:
            widget.setVisible(False)
    
    def toggle_chatbox(self):
        self.chatbox_minimized = not self.chatbox_minimized
        for widget in self.chat_widgets:
            widget.setVisible(not self.chatbox_minimized)
    
    def send_chat_message(self):
        msg = self.chat_input.text().strip()
        if msg:
            self.chat_display.append(f"<b>You:</b> {msg}")
            self.chat_input.clear()
            # Here you would connect to backend processing