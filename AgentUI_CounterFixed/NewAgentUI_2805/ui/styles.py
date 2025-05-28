from PyQt5.QtGui import QColor, QFont, QPalette

# Color palette
COLORS = {
    "primary": "#3674B5",      # Dark blue
    "secondary": "#578FCA",    # Medium blue
    "tertiary": "#A1E3F9",     # Light blue
    "accent": "#D1F8EF",       # Pale cyan
    "background": "#f7f9fa",   # Light grey
    "text": "#222222",         # Dark grey/black
    "button": "#e3e6e8",       # Light grey for buttons
    "highlight": "#4fc3f7",    # Bright blue highlight
    "success": "#43a047",      # Green
    "warning": "#ff9800",      # Orange
    "danger": "#d32f2f",       # Red
    "neutral": "#546e7a",      # Grey-blue
    "white": "#ffffff"
}

# Font settings
FONTS = {
    "default": QFont("Segoe UI", 10),
    "title": QFont("Segoe UI", 16, QFont.Bold),
    "subtitle": QFont("Segoe UI", 12, QFont.Bold),
    "button": QFont("Segoe UI", 10, QFont.Bold),
    "small": QFont("Segoe UI", 9)
}

def setup_application_palette():
    """Create and return application palette"""
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(COLORS["background"]))
    palette.setColor(QPalette.WindowText, QColor(COLORS["text"]))
    palette.setColor(QPalette.Base, QColor(COLORS["white"]))
    palette.setColor(QPalette.AlternateBase, QColor("#f0f0f0"))
    palette.setColor(QPalette.Text, QColor(COLORS["text"]))
    palette.setColor(QPalette.Button, QColor(COLORS["button"]))
    palette.setColor(QPalette.ButtonText, QColor(COLORS["text"]))
    palette.setColor(QPalette.Highlight, QColor(COLORS["highlight"]))
    palette.setColor(QPalette.HighlightedText, QColor(COLORS["white"]))
    return palette

# Stylesheet templates
MENU_STYLE = """
    QMenuBar {
        background: #e3e6e8;
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
"""

# Add other style templates as needed