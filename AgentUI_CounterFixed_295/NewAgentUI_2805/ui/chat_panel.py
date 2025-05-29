from PyQt5.QtWidgets import QWidget,QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLineEdit, QSplitter, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from tools.chatbot.openai_client import OpenAIClient

class ChatPanel(QWidget):
    """Chat interface panel"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.chat_widgets = []
        self.chatbox_minimized = True
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Set minimum width for chat panel
        self.setMinimumWidth(350)
        
        # Set border to differentiate chat panel visually
        self.setStyleSheet("""
            QWidget {
                background: #f7f9fa;
                border-left: 0px solid #e0e0e0;
            }
        """)
        
        # Chat title and minimize button
        chat_title = QLabel("Chat Assistant")
        chat_title.setFont(QFont("Segoe UI", 12, QFont.Bold))
        chat_title.setStyleSheet("color: #3674B5;")
        
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
        chat_header.addWidget(chat_title)
        chat_header.addStretch()
        chat_header.addWidget(minimize_btn)
        layout.addLayout(chat_header)
        
        # Create a main widget to hold both display and input
        chat_main = QWidget()
        chat_main_layout = QVBoxLayout(chat_main)
        chat_main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Chat display area - should take most of the vertical space
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        self.chat_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.chat_display.setStyleSheet("""
            QTextEdit {
                background: #f7f9fa;
                color: #222;
                margin-top: 10px;
                border: 2px solid #1976d2;
                border-radius: 15px;
                font-size: 11pt;
            }
        """)
        chat_main_layout.addWidget(self.chat_display, 1)  # Add stretch factor
        
        # Input area with text field and send button
        input_widget = QWidget()
        input_layout = QHBoxLayout(input_widget)
        input_layout.setContentsMargins(0, 5, 0, 0)
        input_layout.setSpacing(8)  # Add some spacing between input and button
        
        self.chat_input = QTextEdit()
        self.chat_input.setPlaceholderText("What would you like to do today?")
        self.chat_input.setStyleSheet("""
            QTextEdit {
                border: 2px solid #1976d2;
                border-radius: 15px;
                padding: 6px 12px;
                background: #fff;
                color: #222;
                font-size: 9pt;
            }
        """)
        self.chat_input.setMinimumHeight(60)
        self.chat_input.setMaximumHeight(120)
        
        # Create the send button with matching height to input
        send_btn = QPushButton("Send")
        # Set size policy to make height follow the input height
        send_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Ignored)
        send_btn.setFixedWidth(100)  # Fixed width but variable height
        send_btn.setStyleSheet("""
            QPushButton {
                background: #4fc3f7;
                color: #fff;
                border-radius: 15px;
                font-weight: bold;
                padding: 0 8;
                margin: 0;
                font-size: 12pt;
            }
            QPushButton:hover {
                background: #039be5;
            }
        """)
        send_btn.clicked.connect(self.send_chat_message)
        
        input_layout.addWidget(self.chat_input)
        input_layout.addWidget(send_btn)
        
        chat_main_layout.addWidget(input_widget)
        
        # Add the main chat widget to the layout with stretch factor
        layout.addWidget(chat_main, 1)
        
        # Add widgets to list for visibility toggling
        self.chat_widgets = [chat_title, self.chat_display, self.chat_input, send_btn]
        for widget in self.chat_widgets:
            widget.setVisible(True)  # Make visible by default
    
    def toggle_chatbox(self):
        self.chatbox_minimized = not self.chatbox_minimized
        for widget in self.chat_widgets:
            widget.setVisible(not self.chatbox_minimized)
    
    def send_chat_message(self):
        msg = self.chat_input.text().strip()
        chatbot = OpenAIClient() 
        if msg:
            response = chatbot.send_message(msg)
            self.chat_display.append(f"<b>You:</b> {response}")
            self.chat_input.clear()
            # Here you would connect to backend processing