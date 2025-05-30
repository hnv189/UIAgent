"""Utility functions for workspace management"""

from PyQt5.QtWidgets import QFileDialog, QMessageBox

def select_workspace(parent):
    """Open dialog to select workspace directory"""
    ws_dir = QFileDialog.getExistingDirectory(parent, "Open Workspace")
    if ws_dir:
        return ws_dir
    return None

def load_recent_workspaces():
    """Load list of recent workspaces from settings"""
    # This would actually load from settings/config file
    return []

def save_recent_workspace(workspace_path):
    """Save workspace to recent list"""
    # This would save to settings/config file
    pass