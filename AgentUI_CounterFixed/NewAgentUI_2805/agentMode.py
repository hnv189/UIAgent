import sys
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QFrame, QWidget
)
from PyQt5.QtGui import QPainter, QFont, QColor, QPen, QPolygon, QBrush
from PyQt5.QtCore import Qt, QPoint, QRect, QSize, pyqtSignal

class ArrowWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(50, 30)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw arrow line
        painter.setPen(QPen(QColor("#555555"), 2))
        painter.drawLine(0, self.height()//2, self.width()-10, self.height()//2)
        
        # Draw arrowhead
        arrowhead = QPolygon([
            QPoint(self.width()-10, self.height()//2-8),
            QPoint(self.width(), self.height()//2),
            QPoint(self.width()-10, self.height()//2+8)
        ])
        painter.setBrush(QBrush(QColor("#555555")))
        painter.drawPolygon(arrowhead)

class ProcessBox(QFrame):
    def __init__(self, title, color="#1565c0", parent=None):
        super().__init__(parent)
        self.title = title
        self.color = color
        self.setMinimumSize(120, 80)
        self.setMaximumHeight(100)
        self.setFrameShape(QFrame.StyledPanel)
        
        # Apply styling
        self.setStyleSheet(f"""
            ProcessBox {{
                background-color: {color};
                border-radius: 8px;
                border: 2px solid {self._darken_color(color)};
            }}
        """)
        
        # Layout
        layout = QVBoxLayout(self)
        label = QLabel(title)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Segoe UI", 11, QFont.Bold))
        label.setStyleSheet("color: white;")
        layout.addWidget(label)
        
    def _darken_color(self, color):
        """Create a darker version of the color for borders"""
        # Simple approach - this could be more sophisticated
        if color == "#1565c0":  # Blue
            return "#0d47a1"
        elif color == "#43a047":  # Green
            return "#2e7d32"
        elif color == "#e53935":  # Red
            return "#b71c1c"
        return color

class AgenticModeDialog(QDialog):
    accepted_signal = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agentic Mode Confirmation")
        self.setMinimumWidth(500)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Confirm Agentic Development Process")
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #303F9F; margin-bottom: 16px;")
        layout.addWidget(title)
        
        # Description
        description = QLabel("Agentic mode will guide you through the following phases automatically:")
        description.setFont(QFont("Segoe UI", 10))
        description.setAlignment(Qt.AlignCenter)
        layout.addWidget(description)
        
        # Process flow visualization
        flow_layout = QHBoxLayout()
        
        # Unit Design box
        unit_design_box = ProcessBox("Unit Design", "#1565c0")
        flow_layout.addWidget(unit_design_box)
        
        # Arrow 1
        arrow1 = ArrowWidget()
        flow_layout.addWidget(arrow1)
        
        # Code box
        code_box = ProcessBox("Code", "#43a047")
        flow_layout.addWidget(code_box)
        
        # Arrow 2
        arrow2 = ArrowWidget()
        flow_layout.addWidget(arrow2)
        
        # Unit Test box
        unit_test_box = ProcessBox("Unit Test", "#e53935")
        flow_layout.addWidget(unit_test_box)
        
        layout.addLayout(flow_layout)
        
        # Information text
        info_text = QLabel("The system will highlight and guide you through each phase automatically.")
        info_text.setFont(QFont("Segoe UI", 9))
        info_text.setStyleSheet("margin-top: 12px; color: #555; font-style: italic;")
        info_text.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_text)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFont(QFont("Segoe UI", 10))
        cancel_btn.setMinimumWidth(100)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #e0e0e0;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #bdbdbd;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        confirm_btn = QPushButton("Confirm")
        confirm_btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        confirm_btn.setMinimumWidth(100)
        confirm_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        confirm_btn.clicked.connect(self._on_confirm)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(confirm_btn)
        layout.addLayout(button_layout)
        
    def _on_confirm(self):
        self.accepted_signal.emit()
        self.accept()

# Function to be called from MainWindow
def show_agentic_mode_dialog(parent=None):
    """Show the agentic mode dialog and return True if confirmed"""
    dialog = AgenticModeDialog(parent)
    result = dialog.exec_()
    return result == QDialog.Accepted

def highlight_vmodel_buttons(main_window, highlight=True):
    """Highlight the Unit Design, Code, and Unit Test buttons in the V-model"""
    # Indices for Unit Design, Code, Unit Test buttons
    indices = [3, 4, 5]  # 0-based index
    
    for idx, button in enumerate(main_window.v_buttons):
        if idx in indices:
            if highlight:
                # Apply green styling for highlighted buttons
                button.is_active = True
                button.setChecked(True)
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #43a047; /* Green background */
                        color: white;
                        border-radius: 6px;
                        padding: 6px 12px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #388e3c; /* Darker green on hover */
                    }
                """)
            else:
                # Reset styling for unhighlighted buttons
                button.is_active = False
                button.setChecked(False)
                button.setStyleSheet("""
                    QPushButton {
                        background-color: #e0e0e0; /* Grey background */
                        color: black;
                        border-radius: 6px;
                        padding: 6px 12px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #bdbdbd; /* Darker grey on hover */
                    }
                """)
        else:
            # Apply default grey styling to other buttons
            button.is_active = False
            button.setChecked(False)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #e0e0e0; /* Grey background */
                    color: black;
                    border-radius: 6px;
                    padding: 6px 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #bdbdbd; /* Darker grey on hover */
                }
            """)
        button.update()
