from PyQt5.QtWidgets import QFrame, QVBoxLayout, QGridLayout, QLabel, QPushButton, QHBoxLayout,QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal
from ui.custom_widgets import ParallelogramButton
from ui.domain_panel import DomainPanel
from ui.styles import COLORS

class VModelFrame(QFrame):
    """V-Model visualization frame with process buttons"""
    
    # Signals
    tool_count_changed = pyqtSignal(int)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.v_buttons = []
        self.grid_labels = []
        self.tool_count = 0
        self.grid_visible = False
        self.setup_ui()
    
    def setup_ui(self):
        # Frame styling
        self.setStyleSheet("""
            QFrame {
            border: 2px solid #1976d2;
            border-radius: 15px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #e3f2fd, stop:1 #bbdefb);
            margin-top: 0px;
            margin-bottom: 5px;
            }
        """)
        
        # Set size policy to make the frame responsive in both directions
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumHeight(350)
        
        # Main layout
        vmodel_frame_layout = QVBoxLayout(self)
        vmodel_frame_layout.setContentsMargins(18, 18, 18, 18)
        vmodel_frame_layout.setSpacing(0)
        
        # Create grid layout for V-model components with 1 as stretch factor
        vmodel_layout = QGridLayout()
        vmodel_layout.setHorizontalSpacing(0)
        vmodel_layout.setVerticalSpacing(2)
        
        # Add grid to frame layout with stretch
        vmodel_frame_layout.addLayout(vmodel_layout, 1)
        
        # Tool counter and Start button at bottom
        bottom_layout = QHBoxLayout()
        
        # Tool counter (left aligned)
        self.tool_counter_label = QLabel("Tools Selected: 0")
        self.tool_counter_label.setFont(QFont("Segoe UI", 9))
        self.tool_counter_label.setStyleSheet("""
            color: #3674B5;
            background: rgba(255, 255, 255, 150);
            border-radius: 4px;
            padding: 2px 6px;
        """)
        bottom_layout.addWidget(self.tool_counter_label)
        
        # Add stretch to push Start button to the right
        bottom_layout.addStretch(1)
        
        # Create Start button
        self.start_btn = QPushButton("Start")
        self.start_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.start_btn.setMinimumWidth(150)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #43a047;
                color: #fff;
                border-radius: 8px;
                padding: 8px 24px;
                font-size: 13pt;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #388e3c;
            }
        """)
        bottom_layout.addWidget(self.start_btn)
        
        # Add bottom layout to main frame layout
        vmodel_frame_layout.addLayout(bottom_layout)
        
        # Show grid for debugging (initially hidden)
        grid_rows, grid_cols = 6, 21
        self.grid_labels = []
        for row in range(grid_rows):
            row_labels = []
            for col in range(grid_cols):
                grid_label = QLabel(f"{row},{col}")
                grid_label.setStyleSheet("color: #bbb; background: #e3e6e8; border: 1px dashed #b2bec3;")
                grid_label.setAlignment(Qt.AlignCenter)
                grid_label.setVisible(self.grid_visible)
                vmodel_layout.addWidget(grid_label, row, col)
                row_labels.append(grid_label)
            self.grid_labels.append(row_labels)
        
        # Add Agentic Mode and Manual Mode buttons
        self.create_mode_buttons(vmodel_layout)
        
        # Create V-model process buttons
        self.create_v_buttons(vmodel_layout)
        
        # Add Domain Panel
        domain_panel = DomainPanel()
        vmodel_layout.addWidget(domain_panel, 1, 10, 3, 1, alignment=Qt.AlignCenter)
        
        # Set stretch for rows and columns
        for row in range(grid_rows):
            vmodel_layout.setRowStretch(row, 1)
        for col in range(grid_cols):
            vmodel_layout.setColumnStretch(col, 1)
    
    def create_mode_buttons(self, layout):
        """Create Agentic and Manual mode buttons"""
        agentic_mode_btn = QPushButton("Agentic Mode")
        agentic_mode_btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        agentic_mode_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff9800; /* Orange background */
                color: white;
                border-radius: 6px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #fb8c00; /* Darker orange on hover */
            }
            QPushButton:checked {
                background-color: #f57c00; /* Even darker orange when checked */
                border: 2px solid #ffcc00; /* Yellow border when checked */
            }
        """)
        agentic_mode_btn.setCheckable(True)
        agentic_mode_btn.setChecked(True)
        # Position to the left of column 10 (centered at 8-9)
        layout.addWidget(agentic_mode_btn, 0, 7, 1, 3, alignment=Qt.AlignCenter)
        self.agentic_mode_btn = agentic_mode_btn
        
        manual_mode_btn = QPushButton("Manual Mode")
        manual_mode_btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        manual_mode_btn.setStyleSheet("""
            QPushButton {
                background-color: #546e7a;
                color: white;
                border-radius: 6px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #455a64;
            }
            QPushButton:checked {
                background-color: #37474f;
                border: 2px solid #ffcc00;
            }
        """)
        manual_mode_btn.setCheckable(True)
        # Position to the right of column 10 (centered at 11-12)
        layout.addWidget(manual_mode_btn, 0, 11, 1, 3, alignment=Qt.AlignCenter)
        self.manual_mode_btn = manual_mode_btn
    
    def create_v_buttons(self, layout):
        """Create V-model process buttons"""
        # Button labels for V-model
        v_labels = [
            "System Req", "SW Arch", "SW Design", "Unit Design", "Code",
            "Unit Test", "Integration Test", "System Test", "Acceptance Test"
        ]
        
        # Each button (except "Code") takes 2 columns, last grid coordinate is next button's first
        # "Code" button spans columns 9,10,11 at row 4 (0-based index)
        positions = [
            (1, 5, 2),   # System Req: row 1 (was 0), cols 4-5 (shifted left)
            (2, 6, 2),   # SW Arch: row 2, cols 5-6 (shifted left)
            (3, 7, 2),   # SW Design: row 3, cols 6-7 (shifted left)
            (4, 8, 2),   # Unit Design: row 4, cols 7-8 (shifted left)
            (5, 9, 3),   # Code: row 5, cols 9-11 (centered at 10)
            (4, 11, 2),  # Unit Test: row 4, cols 12-13 (shifted right)
            (3, 12, 2),  # Integration Test: row 3, cols 13-14 (shifted right)
            (2, 13, 2),  # System Test: row 2, cols 14-15 (shifted right)
            (1, 14, 2),  # Acceptance Test: row 1, cols 15-16 (shifted right)
        ]
        
        directions = [
            "right", "right", "right", "right",
            "trapezoid",
            "left", "left", "left", "left"
        ]
        
        v_buttons = []
        for i, (row, col, span) in enumerate(positions):
            btn = ParallelogramButton(v_labels[i], direction=directions[i])
            if v_labels[i] == "Code":
                btn.setMinimumWidth(210)
                btn.setMaximumWidth(420)
                btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
            else:
                btn.setMinimumWidth(140)
                btn.setMaximumWidth(280)
                btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
            btn.setMinimumHeight(50)
            btn.setMaximumHeight(60)
            btn.setStyleSheet("margin-left: -18px; margin-right: -18px;")
            btn.clicked.connect(lambda checked=False, idx=i: self.v_button_clicked(idx))
            layout.addWidget(btn, row, col, 1, span, alignment=Qt.AlignCenter)
            v_buttons.append(btn)
        self.v_buttons = v_buttons
    
    def v_button_clicked(self, idx):
        """Handle V-model button clicks"""
        # Find the button that was clicked
        button = self.v_buttons[idx]
        
        # Get current state of the button
        is_checked = button.isChecked()
        
        if is_checked and not button.is_active:
            # Button was just checked
            self.tool_count += 1
            button.is_active = True
        elif not is_checked and button.is_active:
            # Button was just unchecked
            if self.tool_count > 0:
                self.tool_count -= 1
            button.is_active = False
        
        # Update the counter label
        self.tool_counter_label.setText(f"Tools Selected: {self.tool_count}")
        
        # Emit signal
        self.tool_count_changed.emit(self.tool_count)
        
        # Force repaint the button
        button.update()
        
        print(f"V-model button clicked: {button.text()}, Tools: {self.tool_count}")
    
    # def toggle_grid_visibility(self):
    #     """Toggle grid visibility for debugging"""
    #     self.grid_visible = not self.grid_visible
    #     for row in self.grid_labels:
    #         for label in row:
    #             label.setVisible(self.grid_visible)