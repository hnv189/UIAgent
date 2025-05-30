from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class DomainPanel(QWidget):
    """Domain selection panel for ASW/BSW"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        self.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #e3f2fd, stop:1 #bbdefb);
            border: 0px solid #42a5f5;
            border-radius: 12px;
            padding: 6px 8px;
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(6)

        # Add working domain label
        working_domain_label = QLabel("Working Domain")
        working_domain_label.setAlignment(Qt.AlignCenter)
        working_domain_label.setFont(QFont("Segoe UI", 8, QFont.Bold))
        working_domain_label.setStyleSheet("""
            color: #000000; 
            background: #bbdefb; 
            border: none;
            border-radius: 4px;
            padding: 2px;
        """)
        layout.addWidget(working_domain_label)

        # ASW checkbox
        self.asw_checkbox = QCheckBox("ASW")
        self.asw_checkbox.setFont(QFont("Segoe UI", 9, QFont.Bold))
        self.asw_checkbox.setStyleSheet("""
            QCheckBox {
                background: #ffcdd2;
                color: #000000;
                border: 2px solid #d32f2f;
                border-radius: 4px;
                padding: 2px 4px;
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #d32f2f;
                background: white;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #d32f2f;
                background: #d32f2f;
            }
        """)
        layout.addWidget(self.asw_checkbox)

        # BSW checkbox
        self.bsw_checkbox = QCheckBox("BSW")
        self.bsw_checkbox.setFont(QFont("Segoe UI", 9, QFont.Bold))
        self.bsw_checkbox.setStyleSheet("""
            QCheckBox {
                background: #c8e6c9;
                color: #000000;
                border: 2px solid #2e7d32;
                border-radius: 4px;
                padding: 2px 4px;
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #2e7d32;
                background: white;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #2e7d32;
                background: #2e7d32;
            }
        """)
        layout.addWidget(self.bsw_checkbox)