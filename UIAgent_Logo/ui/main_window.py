import os
import sys
from PyQt5.QtWidgets import (
    QMainWindow, QAction, QFileDialog, QMessageBox, QWidget, QVBoxLayout, 
    QHBoxLayout, QLabel,QSizePolicy, QPushButton, QCheckBox, QComboBox, QLineEdit,QSplitter
)
from PyQt5.QtGui import QFont, QPixmap

from PyQt5.QtCore import Qt

# Import our modules
from ui.styles import setup_application_palette, MENU_STYLE, FONTS, COLORS
from ui.v_model_frame import VModelFrame
from ui.chat_panel import ChatPanel
from utils.workspace import select_workspace, load_recent_workspaces
import agentMode

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agentic Development Assistant")
        self.resize(1200, 600)
        
        # Set up UI components
        self.setup_palette()
        self.setup_menu()
        self.setup_central()
        self.setup_statusbar()
    
    def setup_palette(self):
        """Set application palette"""
        palette = setup_application_palette()
        self.setPalette(palette)
        self.setFont(FONTS["default"])
    
    def setup_menu(self):
        """Set up menu bar"""
        menubar = self.menuBar()
        menubar.setStyleSheet(MENU_STYLE)
        # File menu
        file_menu = menubar.addMenu("File")
        
        openws_action = QAction("OpenWS", self)
        openws_action.triggered.connect(self.open_workspace)
        file_menu.addAction(openws_action)

        recentws_action = QAction("RecentWS", self)
        recentws_action.triggered.connect(self.show_recent_workspaces)
        file_menu.addAction(recentws_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        documentation_action = QAction("Documentation", self)
        documentation_action.triggered.connect(self.show_documentation)
        help_menu.addAction(documentation_action)
    
    def setup_central(self):
        """Set up central widget with main UI components"""
        central = QWidget()
        main_layout = QHBoxLayout(central)  # Change to horizontal layout
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Create a splitter to divide left and right panels
        splitter = QSplitter(Qt.Horizontal)
        
        # Make the splitter handle more visible and adjustable
        splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #e0e0e0;
                width: 0px;
            }
            QSplitter::handle:hover {
                background-color: #1976d2;
            }
        """)
        
        # Left panel (workflow configuration)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create header with workflow label and class selector
        self.create_header(left_layout)
        
        # Add spacer
        spacer = QWidget()
        spacer.setFixedHeight(10)
        left_layout.addWidget(spacer)
        
        # Create V-model frame with responsive size policy
        self.v_model_frame = VModelFrame()
        self.v_model_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.v_model_frame.setMinimumHeight(350)
        self.v_model_frame.tool_count_changed.connect(self.update_tool_count)

        # Connect mode buttons
        self.v_model_frame.agentic_mode_btn.clicked.connect(self.toggle_agentic_mode)
        self.v_model_frame.manual_mode_btn.clicked.connect(self.toggle_manual_mode)
        
        # Connect Start button
        self.v_model_frame.start_btn.clicked.connect(self.start_workflow)
        
        # Add V-model frame with STRETCH to make it fill available space
        left_layout.addWidget(self.v_model_frame, 1) # 1 = stretch factor
        
        # Add left panel to splitter
        splitter.addWidget(left_panel)
        
        # Right panel (chat panel)
        self.chat_panel = ChatPanel()
        
        # Make the chat panel take the full height
        self.chat_panel.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        
        # Make chat widgets visible by default
        for widget in self.chat_panel.chat_widgets:
            widget.setVisible(True)
        self.chat_panel.chatbox_minimized = False
        
        splitter.addWidget(self.chat_panel)
        
        # Set initial sizes (70% left, 30% right)
        splitter.setSizes([700, 300])
        
        # Add splitter to main layout
        main_layout.addWidget(splitter)
        
        self.setCentralWidget(central)
    
    def create_header(self, layout):
        """Create header with workflow label and class selector"""
        header_layout = QHBoxLayout()
        
        # "Workflow Configuration" label
        workflow_label = QLabel("Workflow configuration:")
        workflow_label.setFont(FONTS["title"])
        workflow_label.setStyleSheet(f"color: {COLORS['primary']}; margin-top: 0px; margin-bottom: 0px;")
        header_layout.addWidget(workflow_label)
        
        # Add spacer to push class selector to the right
        header_layout.addStretch(1)
        
        # Class selector
        # class_selector_layout = QHBoxLayout()
        # class_selector_label = QLabel("Select Class:")
        # class_selector_label.setFont(FONTS["button"])
        
        # class_selector = QComboBox()
        # class_selector.setFixedWidth(300)
        # class_selector.setFont(FONTS["default"])
        # class_selector.setStyleSheet(f"""
        #     QComboBox {{
        #         border: 1px solid {COLORS['primary']};
        #         border-radius: 4px;
        #         padding: 3px;
        #         background: white;
        #     }}
        #     QComboBox:hover {{
        #         border: 1px solid {COLORS['secondary']};
        #     }}
        #     QComboBox::drop-down {{
        #         subcontrol-origin: padding;
        #         subcontrol-position: top right;
        #         width: 20px;
        #         border-left: 1px solid {COLORS['primary']};
        #         border-top-right-radius: 3px;
        #         border-bottom-right-radius: 3px;
        #     }}
        # """)
        
        # # Add sample classes
        # sample_classes = [
        #     "Select a class...",
        #     "VehicleDynamicsControl", 
        #     "EngineManagement", 
        #     "TransmissionControl",
        #     "BrakeSystemControl",
        #     "SteeringAssistant",
        #     "ActiveSuspension"
        # ]
        
        # for cls in sample_classes:
        #     class_selector.addItem(cls)
        
        # class_selector_layout.addWidget(class_selector_label)
        # class_selector_layout.addWidget(class_selector)
        
        # header_layout.addLayout(class_selector_layout)
        layout.addLayout(header_layout)
    
    def setup_statusbar(self):
        """Set up status bar"""
        status_bar = self.statusBar()
        status_bar.showMessage("Current WorkSpace: MS_ESP_10_VDC")
        status_bar.setStyleSheet(f"""
            QStatusBar {{
                background: {COLORS['background']};
                color: {COLORS['text']};
                border-top: 1px solid {COLORS['button']};
            }}
        """)
        
        # To right-align, add a stretchable QLabel
        right_label = QLabel("Reading Header File...")
        right_label.setStyleSheet(f"color: {COLORS['text']}; padding-right: 12px;")
        status_bar.addPermanentWidget(right_label)
        self.right_status_label = right_label
    
    def update_tool_count(self, count):
        """Update tool count when V-model buttons are clicked"""
        self.tool_count = count
    def start_workflow(self):
        """Handle Start button click"""
        if self.v_model_frame.tool_count > 0:
            QMessageBox.information(self, "Workflow Started", 
                                f"Starting workflow with {self.v_model_frame.tool_count} tools selected")
            # Here you would add the actual workflow start logic
        else:
            QMessageBox.warning(self, "No Tools Selected", 
                            "Please select at least one tool before starting the workflow.")
    def toggle_agentic_mode(self):
        """Toggle agentic mode"""
        sender = self.sender()
        if sender.isChecked():
            if agentMode.show_agentic_mode_dialog(self):
                # User confirmed, highlight the buttons
                agentMode.highlight_vmodel_buttons(self.v_model_frame, True)
                # Uncheck manual mode
                self.v_model_frame.manual_mode_btn.setChecked(False)
                self.v_model_frame.tool_count = 3  # Ensure tool_count is updated
                self.update_tool_count(self.v_model_frame.tool_count)  # Update tool count in the UI
                self.v_model_frame.tool_counter_label.setText(f"Tools Selected: {self.v_model_frame.tool_count}")
            else:
                # User canceled, revert the button state
                sender.setChecked(False)
        else:
            # Uncheck manual mode if agentic mode is turned off
            self.v_model_frame.manual_mode_btn.setChecked(False)
            agentMode.highlight_vmodel_buttons(self.v_model_frame, False)
            self.v_model_frame.tool_count = 0  # Reset tool_count
            self.update_tool_count(self.v_model_frame.tool_count)  # Update tool count in the UI
            self.v_model_frame.tool_counter_label.setText(f"Tools Selected: {self.v_model_frame.tool_count}")

    
    def toggle_manual_mode(self):
        """Toggle manual mode"""
        if self.sender().isChecked():
            QMessageBox.information(self, "Manual Mode", "Please select at least 1 tool for the workflow and press START button.")
            agentMode.highlight_vmodel_buttons(self.v_model_frame, False)
            self.v_model_frame.agentic_mode_btn.setChecked(False)
    
    def open_workspace(self):
        """Open workspace directory dialog"""
        ws_dir = select_workspace(self)
        if ws_dir:
            QMessageBox.information(self, "Workspace Opened", f"Opened workspace: {ws_dir}")
            # Update status bar
            self.statusBar().showMessage(f"Current WorkSpace: {os.path.basename(ws_dir)}")
    
    def show_recent_workspaces(self):
        """Show recent workspaces dialog"""
        recent = load_recent_workspaces()
        if not recent:
            QMessageBox.information(self, "Recent Workspaces", "No recent workspaces found.")
        # else show dialog with recent workspaces
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About Agentic Tool",
            "<h3>Agentic Tool</h3>"
            "<p>Version 1.0</p>"
            "<p>A model-based effort agent tool for software development</p>"
            "<p>© 2023 Automotive Software</p>"
        )
    
    def show_documentation(self):
        """Show documentation dialog"""
        QMessageBox.information(
            self,
            "Documentation",
            "Documentation will open in your browser.\n"
            "For now, this is a placeholder."
        )