from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QFont, QPainter, QColor, QPolygon
from PyQt5.QtCore import Qt, QPoint
from ui.styles import COLORS

class ParallelogramButton(QPushButton):
    """Custom button with parallelogram or trapezoid shape for V-model visualization"""
    
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
            painter.setBrush(QColor(COLORS["success"]))  # Green background
            painter.setPen(QColor("#2e7d32"))           # Darker green border
        else:
            painter.setBrush(QColor(COLORS["primary"]))  # Default blue
            painter.setPen(QColor("#0d47a1"))           # Default border
            
        painter.drawPolygon(polygon)
        painter.setPen(QColor(COLORS["white"]))
        painter.setFont(QFont("Segoe UI", 9, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())