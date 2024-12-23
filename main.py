import sys
from PyQt5.QtWidgets import QApplication
from src.gui.main_window import ZipCracker


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ZipCracker()
    window.show()
    sys.exit(app.exec_())
