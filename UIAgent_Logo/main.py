import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow
from PyQt5.QtGui import QIcon

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(r"C:\Users\PC\Desktop\UIAgent\assets\logo\copilot-color.png"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())