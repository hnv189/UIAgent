import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QFileDialog, QMenu, QMessageBox, QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox,QVBoxLayout, QWidget, QFrame
)
from PyQt5.QtGui import QFont, QPalette, QColor, QPainter, QPolygon, QColor, QFont
from PyQt5.QtCore import Qt, QPoint
import agentMode


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agentic Development Assistant")
        self.resize(900, 600)
        self.tool_count = 0  
        self.setup_palette()
        self.setup_menu()
        self.setup_central()
        self.setup_statusbar()

    def setup_palette(self):
        # Bright, modern, flat palette
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#f7f9fa"))
        palette.setColor(QPalette.WindowText, QColor("#222222"))
        palette.setColor(QPalette.Base, QColor("#ffffff"))
        palette.setColor(QPalette.AlternateBase, QColor("#f0f0f0"))
        palette.setColor(QPalette.Text, QColor("#222222"))
        palette.setColor(QPalette.Button, QColor("#e3e6e8"))
        palette.setColor(QPalette.ButtonText, QColor("#222222"))
        palette.setColor(QPalette.Highlight, QColor("#4fc3f7"))
        palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))
        self.setPalette(palette)
        self.setFont(QFont("Segoe UI", 10))

    def setup_menu(self):
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background: #e3e6e8;      /* Different from window background */
                border: none;
                color: #222;
            }
            QMenuBar::item {
                background: transparent;
                padding: 8px 18px;
                margin: 0 2px;
            }
            QMenuBar::item:selected {
                background: #b2ebf2;
                border-radius: 4px;
            }
            QMenu {
                background: #ffffff;
                border: 1px solid #e3e6e8;
            }
            QMenu::item {
                padding: 8px 24px;
            }
            QMenu::item:selected {
                background: #4fc3f7;
                color: #fff;
            }
        """)
        file_menu = menubar.addMenu("File")
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        # Add actions to the Help menu
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        documentation_action = QAction("Documentation", self)
        documentation_action.triggered.connect(self.show_documentation)
        help_menu.addAction(documentation_action)
        
        openws_action = QAction("OpenWS", self)
        openws_action.triggered.connect(self.open_workspace)
        file_menu.addAction(openws_action)

        recentws_action = QAction("RecentWS", self)
        recentws_action.triggered.connect(self.show_recent_workspaces)
        file_menu.addAction(recentws_action)
    def show_about(self):
        QMessageBox.about(
            self,
            "About Agentic Tool",
            "<h3>Agentic Tool</h3>"
            "<p>Version 1.0</p>"
            "<p>A model-based effort agent tool for software development</p>"
            "<p>© 2023 Automotive Software</p>"
        )
        
    def show_documentation(self):
        # In a real application, you might open a documentation window or launch a browser
        QMessageBox.information(
            self,
            "Documentation",
            "Documentation will open in your browser.\n"
            "For now, this is a placeholder."
        )
    def setup_statusbar(self):
        status_bar = self.statusBar()
        status_bar.showMessage("Current WorkSpace: MS_ESP_10_VDC")
        # Align the status bar text to the right
        status_bar.setStyleSheet("""
            QStatusBar {
                background: #f7f9fa;
                color: #222;
                border-top: 1px solid #e3e6e8;
            }
        """)
        # To right-align, add a stretchable QLabel
        from PyQt5.QtWidgets import QLabel
        right_label = QLabel("Reading Header File...")
        right_label.setStyleSheet("color: #222; padding-right: 12px;")
        status_bar.addPermanentWidget(right_label)
        self.right_status_label = right_label
    def toggle_agentic_mode(self):
        if self.sender().isChecked():
            if agentMode.show_agentic_mode_dialog(self):
                # User confirmed, highlight the buttons
                agentMode.highlight_vmodel_buttons(self, True)
                # Uncheck manual mode
                for btn in self.findChildren(QPushButton):
                    if btn.text() == "Manual Mode":
                        btn.setChecked(False)
            else:
                # User canceled, revert the button state
                self.sender().setChecked(False)

    def toggle_manual_mode(self):
        if self.sender().isChecked():
            # Turn off agentic mode and unhighlight buttons
            agentMode.highlight_vmodel_buttons(self, False)
            # Uncheck agentic mode
            for btn in self.findChildren(QPushButton):
                if btn.text() == "Agentic Mode":
                    btn.setChecked(False)
    def setup_central(self):
        from PyQt5.QtWidgets import QTextEdit, QLineEdit, QPushButton, QHBoxLayout, QGridLayout, QLabel, QCheckBox, QComboBox

        central = QWidget()
        main_layout = QVBoxLayout()
        # Create a horizontal layout for the header section
        header_layout = QHBoxLayout()
        
        # "Workflow Configuration" label on the left
        workflow_label = QLabel("WORKFLOW CONFIGURATION:")
        workflow_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        workflow_label.setStyleSheet("""
            color: #3674B5;
            margin-top: 12px;
            margin-bottom: 0px;
        """)
        header_layout.addWidget(workflow_label)
        
        # Add spacer to push class selector to the right
        header_layout.addStretch(1)
        
        # Class selector on the right
        class_selector_layout = QHBoxLayout()
        class_selector_label = QLabel("Select Class:")
        class_selector_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        
        class_selector = QComboBox()
        class_selector.setFixedWidth(300)
        class_selector.setFont(QFont("Segoe UI", 10))
        class_selector.setStyleSheet("""
            QComboBox {
                border: 1px solid #3674B5;
                border-radius: 4px;
                padding: 4px 8px;
                background: white;
            }
            QComboBox:hover {
                border: 1px solid #578FCA;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #3674B5;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QComboBox::down-arrow {
                width: 14px;
                height: 14px;
            }
        """)
        
        # Add some sample class items
        sample_classes = [
            "Select a class...",
            "VehicleDynamicsControl", 
            "EngineManagement", 
            "TransmissionControl",
            "BrakeSystemControl",
            "SteeringAssistant",
            "ActiveSuspension"
        ]
        
        for cls in sample_classes:
            class_selector.addItem(cls)
        
        class_selector_layout.addWidget(class_selector_label)
        class_selector_layout.addWidget(class_selector)
        
        # Add class selector layout to header layout
        header_layout.addLayout(class_selector_layout)
        
        # Add the header layout to the main layout
        main_layout.addLayout(header_layout)
        
        # Add some spacing after the header
        spacer = QWidget()
        spacer.setFixedHeight(10)  # 10 pixels of vertical space
        main_layout.addWidget(spacer)
        
        main_layout.addStretch(1)

        vmodel_frame = QFrame()
        vmodel_frame.setStyleSheet("""
            QFrame {
                border: 3px solid #1976d2;
                border-radius: 32px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #e3f2fd, stop:1 #bbdefb);
                margin-top: 12px;
                margin-bottom: 12px;
            }
        """)
        vmodel_frame_layout = QVBoxLayout(vmodel_frame)
        vmodel_frame_layout.setContentsMargins(18, 18, 18, 18)
        vmodel_frame_layout.setSpacing(0)
        
        # Create vmodel_layout
        vmodel_layout = QGridLayout()
        vmodel_layout.setHorizontalSpacing(0)
        vmodel_layout.setVerticalSpacing(2)
        
        # First add the grid to the frame layout
        vmodel_frame_layout.addLayout(vmodel_layout)
        
        # Then create a separate horizontal layout for the counter only
        counter_layout = QHBoxLayout()
        self.tool_counter_label = QLabel("Tools Selected: 0")
        self.tool_counter_label.setFont(QFont("Segoe UI", 9))
        self.tool_counter_label.setStyleSheet("""
            color: #3674B5;
            background: rgba(255, 255, 255, 150);
            border-radius: 4px;
            padding: 2px 6px;
        """)
        counter_layout.addStretch(1)
        counter_layout.addWidget(self.tool_counter_label)
        
        # Add counter layout after the grid layout
        vmodel_frame_layout.addLayout(counter_layout)
        # Add the grid layout to the frame
        vmodel_frame_layout.addLayout(vmodel_layout)

        # Show grid for debugging: fill all grid cells with a faint label
        grid_rows, grid_cols = 6, 21
        self.grid_labels = []
        for row in range(grid_rows):
            row_labels = []
            for col in range(grid_cols):
                grid_label = QLabel(f"{row},{col}")
                grid_label.setStyleSheet("color: #bbb; background: #e3e6e8; border: 1px dashed #b2bec3;")
                grid_label.setAlignment(Qt.AlignCenter)
                vmodel_layout.addWidget(grid_label, row, col)
                row_labels.append(grid_label)
            self.grid_labels.append(row_labels)
        # Add Agentic Mode and Manual Mode buttons in the top row
        # Add Agentic Mode and Manual Mode buttons in the top row, symmetric around column 10
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
        vmodel_layout.addWidget(agentic_mode_btn, 0, 7, 1, 3, alignment=Qt.AlignCenter)
        
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
        agentic_mode_btn.clicked.connect(self.toggle_agentic_mode)
        manual_mode_btn.clicked.connect(self.toggle_manual_mode)
        # Position to the right of column 10 (centered at 11-12)
        vmodel_layout.addWidget(manual_mode_btn, 0, 11, 1, 3, alignment=Qt.AlignCenter)
        
        # Button labels for V-model
        v_labels = [
            "System Req", "SW Arch", "SW Design", "Unit Design", "Code",
            "Unit Test", "Integration Test", "System Test", "Acceptance Test"
        ]
        v_buttons = []
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
            vmodel_layout.addWidget(btn, row, col, 1, span, alignment=Qt.AlignCenter)
            v_buttons.append(btn)
        self.v_buttons = v_buttons
        for row in range(grid_rows):
            vmodel_layout.setRowStretch(row, 1)
        for col in range(grid_cols):
            vmodel_layout.setColumnStretch(col, 1)

        main_layout.addStretch(1)
        main_layout.addWidget(vmodel_frame)
        
        
        
        # --- Start button
        start_btn = QPushButton("Start")
        start_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        start_btn.setMinimumWidth(210)
        start_btn.setStyleSheet("""
            QPushButton {
                background-color: #43a047;
                color: #fff;
                border-radius: 8px;
                padding: 8px 24px;
                font-size: 13pt;
                font-weight: bold;
                margin-top: 18px; /* Extra space from Code button */
            }
            QPushButton:hover {
                background-color: #388e3c;
            }
        """)
        
        main_layout.addWidget(start_btn,alignment=Qt.AlignCenter)
        # --- Chatbox area at the bottom ---
        chat_layout = QVBoxLayout()

        # Minimize/Expand button
        self.chatbox_minimized = False
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
        chat_layout.addLayout(chat_header)

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
        chat_layout.addWidget(self.chat_display)
        
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
        self.chat_input.returnPressed.connect(send_btn.click)

        input_row.addWidget(self.chat_input)
        input_row.addWidget(send_btn)
        chat_layout.addLayout(input_row)

        self.chat_widgets = [self.chat_display, self.chat_input, send_btn]
        for widget in self.chat_widgets:
            widget.setVisible(False)

        main_layout.addLayout(chat_layout)
        central.setLayout(main_layout)
        self.setCentralWidget(central)
        
        domain_group = QWidget()
        domain_group.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                stop:0 #e3f2fd, stop:1 #bbdefb);
            border: 0px solid #42a5f5;
            border-radius: 12px;
            padding: 6px 8px;
        """)
        domain_layout = QVBoxLayout(domain_group)
        domain_layout.setContentsMargins(4, 4, 4, 4)
        domain_layout.setSpacing(6)

        # Add your widgets to the group
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
        domain_layout.addWidget(working_domain_label)

        asw_checkbox = QCheckBox("ASW")
        asw_checkbox.setFont(QFont("Segoe UI", 9, QFont.Bold))
        asw_checkbox.setStyleSheet("""
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
        domain_layout.addWidget(asw_checkbox)

        bsw_checkbox = QCheckBox("BSW")
        bsw_checkbox.setFont(QFont("Segoe UI", 9, QFont.Bold))
        bsw_checkbox.setStyleSheet("""
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
        domain_layout.addWidget(bsw_checkbox)

        # Add the group widget to the grid, spanning 3 rows at column 10
        vmodel_layout.addWidget(domain_group, 1, 10, 3, 1, alignment=Qt.AlignCenter)
        # --- Grid visibility switch ---
        self.grid_visible = False
        grid_switch = QCheckBox("Show Grid")
        grid_switch.setChecked(True)
        grid_switch.setStyleSheet("margin-left: 12px;")
        main_layout.addWidget(grid_switch, alignment=Qt.AlignLeft)

        def toggle_grid():
            self.grid_visible = not self.grid_visible
            for row in self.grid_labels:
                for label in row:
                    label.setVisible(self.grid_visible)
        grid_switch.stateChanged.connect(toggle_grid)
    def v_button_clicked(self, idx):
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
        
        # Force repaint the button
        button.update()
        
        print(f"V-model button clicked: {button.text()}, Tools: {self.tool_count}")
    def open_workspace(self):
        ws_dir = QFileDialog.getExistingDirectory(self, "Open Workspace")
        if ws_dir:
            QMessageBox.information(self, "Workspace Opened", f"Opened workspace: {ws_dir}")

    def show_recent_workspaces(self):
        # Placeholder for recent workspaces logic
        QMessageBox.information(self, "Recent Workspaces", "No recent workspaces found.")
        
    def send_chat_message(self):
        msg = self.chat_input.text().strip()
        if msg:
            self.chat_display.append(f"<b>You:</b> {msg}")
            self.chat_input.clear()
    def toggle_chatbox(self):
        self.chatbox_minimized = not self.chatbox_minimized
        for widget in self.chat_widgets:
            widget.setVisible(not self.chatbox_minimized)
            
class ParallelogramButton(QPushButton):
    def __init__(self, text, direction="left", parent=None):
        super().__init__(text, parent)
        self.direction = direction  # "left", "right", or "trapezoid"
        self.is_active = False
        self.setCheckable(True)
    
    def toggle_active(self):
        self.update()  # Force repaint

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        w, h = self.width(), self.height()
        offset = 10  # smaller slant for smaller width
        
        if self.direction == "left":
            polygon = QPolygon([
                QPoint(offset, 0),
                QPoint(w, 0),
                QPoint(w - offset, h),
                QPoint(0, h)
            ])
        elif self.direction == "right":
            polygon = QPolygon([
                QPoint(0, 0),
                QPoint(w - offset, 0),
                QPoint(w, h),
                QPoint(offset, h)
            ])
        elif self.direction == "trapezoid":
            t_offset = 10
            # Upside-down isosceles trapezoid
            polygon = QPolygon([
                QPoint(0, 0),
                QPoint(w, 0),
                QPoint(w - t_offset, h),
                QPoint(t_offset, h)
            ])
        else:
            polygon = QPolygon([
                QPoint(0, 0),
                QPoint(w, 0),
                QPoint(w, h),
                QPoint(0, h)
            ])
        
        # Use green color when button is active (clicked)
        if self.is_active:
            painter.setBrush(QColor("#43a047"))  # Green background
            painter.setPen(QColor("#2e7d32"))    # Darker green border
        else:
            painter.setBrush(QColor("#1565c0"))  # Default blue
            painter.setPen(QColor("#0d47a1"))    # Default border
            
        painter.drawPolygon(polygon)
        painter.setPen(QColor("#fff"))
        painter.setFont(QFont("Segoe UI", 9, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())