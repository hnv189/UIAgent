import sys
import time
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QWidget, QMenuBar, QMenu, QFileDialog, QMessageBox, QStatusBar, QGridLayout, QScrollArea, QTextEdit, QPushButton, QVBoxLayout, QStackedWidget
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPalette, QAction


class StepThread(QThread):
    done = pyqtSignal(str)

    def __init__(self, step_name):
        super().__init__()
        self.step_name = step_name

    def run(self):
        time.sleep(0.5)  # Simulate a delay
        self.done.emit(self.step_name)


class VModelUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("V Model UI - PyQt6")
        self.setGeometry(100, 100, 900, 600)
        self.set_dark_theme()
        self.steps = [
            "Requirements", "Design", "Implementation", "Coding",
            "Unit Testing", "Integration", "Validation"
        ]
        self.buttons = {}
        self.init_ui()

    def set_dark_theme(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#1e1e1e"))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("#ffffff"))
        palette.setColor(QPalette.ColorRole.Button, QColor("#2d2d2d"))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor("#ffffff"))
        palette.setColor(QPalette.ColorRole.Base, QColor("#1e1e1e"))
        palette.setColor(QPalette.ColorRole.Text, QColor("#ffffff"))
        palette.setColor(QPalette.ColorRole.Highlight, QColor("#555555"))
        QApplication.instance().setPalette(palette)

        # Apply stylesheet for modern menu and buttons
        self.setStyleSheet("""
            QMenuBar {
                background-color: #2b2b2b;
                color: white;
            }
            QMenuBar::item {
                background-color: #2b2b2b;
                color: white;
                padding: 4px 10px;
            }
            QMenuBar::item:selected {
                background-color: #555555;
            }
            QMenu {
                background-color: #2b2b2b;
                color: white;
            }
            QMenu::item:selected {
                background-color: #555555;
            }
            QPushButton {
                background-color: #3c3c3c;
                border: 1px solid #555;
                color: white;
                border-radius: 5px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #505050;
            }
        """)

    def init_ui(self):
        self._create_menu_bar()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Use absolute positioning
        self.workspace_label = QLabel("Current workspace: None", central_widget)
        self.workspace_label.setFont(QFont("Arial", 8))
        self.workspace_label.setStyleSheet("color: grey;")
        self.workspace_label.move(10, 10)  # Position at (10, 10)

        # Workspace label layout
        workspace_layout = QHBoxLayout()
        workspace_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for absolute alignment
        self.workspace_label = QLabel("Current workspace: None")
        self.workspace_label.setFont(QFont("Arial", 8))
        self.workspace_label.setStyleSheet("color: grey;")
        workspace_layout.addWidget(self.workspace_label, alignment=Qt.AlignmentFlag.AlignLeft)

        light_colors = [
            "#FFCCCC",  # Light red
            "#FFDD99",  # Light orange
            "#FFFFCC",  # Light yellow
            "#CCFFCC",  # Light green
            "#CCFFFF",  # Light cyan
            "#CCCCFF",  # Light blue
            "#FFCCFF"   # Light pink
        ]
        # Create buttons for V-Model steps
        self.button_positions = [
            (0.2, 0.1),  # Requirements (top-left)
            (0.3, 0.2),  # Design (middle-left)
            (0.4, 0.3),  # Implementation (bottom-left)
            (0.5, 0.4),  # Coding (bottom-center)
            (0.6, 0.3),  # Unit Testing (bottom-right)
            (0.7, 0.2),  # Integration (middle-right)
            (0.8, 0.1)   # Validation (top-right)
        ]
        self.buttons = {}

        for i, (rel_x, rel_y) in enumerate(self.button_positions):
            step = self.steps[i]
            btn = QPushButton(step, self)
            btn.setFixedSize(140, 40)
            btn.setStyleSheet(f"background-color: {light_colors[i]}; color: black;")  # Set initial light color
            btn.clicked.connect(self.create_step_handler(step))
            self.buttons[step] = (btn, rel_x, rel_y)  # Store button and relative positions

        # Status bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.status_label = QLabel("No step in progress")
        self.status_label.setFont(QFont("Arial", 10))
        self.status.addPermanentWidget(self.status_label)

        # Chat box layout
        chat_layout = QHBoxLayout()

        # Chat box
        self.chat_box = QTextEdit(self)
        self.chat_box.setPlaceholderText("Enter your message here...")
        self.chat_box.setFixedHeight(50)
        self.chat_box.setStyleSheet("""
            background-color: lightgrey;
            border: 1px solid white;
            color: black;
        """)
        chat_layout.addWidget(self.chat_box)

        # Send button
        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(self.send_message)
        chat_layout.addWidget(self.send_button)


        # Position buttons initially
        self.reposition_buttons()

    def send_message(self):
        """Handle sending a message from the chat box."""
        message = self.chat_box.toPlainText().strip()
        if message:
            QMessageBox.information(self, "Chat Message", f"You sent: {message}")
            self.chat_box.clear()
    def create_step_handler(self, step_name):
        def handler():
            self.status_label.setText(f"I'm doing {step_name}")
            self.thread = StepThread(step_name)
            self.thread.done.connect(lambda: self.on_step_done(step_name))
            self.thread.start()
        return handler

    def on_step_done(self, step_name):
        QMessageBox.information(self, "Step Done", f"{step_name} completed!")
        btn, _, _ = self.buttons[step_name]
        btn.setStyleSheet("background-color: green; color: white;")  # Change to "well-done" color
        self.status_label.setText(f"Finished: {step_name}")


    def resizeEvent(self, event):
        """Reposition buttons dynamically when the window is resized."""
        super().resizeEvent(event)
        self.reposition_buttons()

    def reposition_buttons(self):
        """Recalculate button positions to keep the V-Model centered in the window."""
        width = self.width()
        height = self.height()

        center_x = width // 2  # Horizontal center of the window
        center_y = height // 2  # Vertical center of the window

        # Define relative positions for the V-Model shape
        relative_positions = [
            (-300, -150),  # Requirements (top-left)
            (-200, -100),  # Design (middle-left)
            (-100, -50),   # Implementation (bottom-left)
            (0, 0),        # Coding (bottom-center)
            (100, -50),    # Unit Testing (bottom-right)
            (200, -100),   # Integration (middle-right)
            (300, -150)    # Validation (top-right)
        ]

        for i, (offset_x, offset_y) in enumerate(relative_positions):
            step = self.steps[i]
            btn, _, _ = self.buttons[step]
            x = center_x + offset_x - btn.width() // 2
            y = center_y + offset_y - btn.height() // 2
            btn.move(x, y)

    def _create_menu_bar(self):
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        file_menu = QMenu("File", self)
        open_action = QAction("Open Workspace", self)
        open_action.triggered.connect(self.open_workspace)
        recent_action = QAction("Recent Workspace", self)
        recent_action.triggered.connect(lambda: self.workspace_label.setText("Recent workspace: ProjectX"))
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(open_action)
        file_menu.addAction(recent_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        menu_bar.addMenu(file_menu)

    def open_workspace(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Workspace")
        if file_name:
            self.workspace_label.setText(f"Current workspace: {file_name}")


def main():
    app = QApplication(sys.argv)
    window = VModelUI()
    window.show()
    sys.exit(app.exec())
if __name__ == "__main__":
    main()
