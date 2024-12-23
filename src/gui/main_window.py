from qfluentwidgets import FluentWindow, FluentIcon, setTheme, Theme
from src.gui.zip_cracker_interface import ZipCrackerInterface
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtCore import Qt


class ZipCracker(FluentWindow):
    """
    This class is the main window of the application.

    It is responsible for setting up the window, including its size,
    title, and contents. It also sets the theme of the application
    to light.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zip Cracker")
        self.resize(700, 800)
        self.setMinimumWidth(700)
        self.center_on_screen()
        self.zip_interface = ZipCrackerInterface(self)
        self.addSubInterface(
            self.zip_interface, icon=FluentIcon.FOLDER, text="Zip Cracker"
        )

        setTheme(Theme.LIGHT)

    def center_on_screen(self):
        """
        Center the window on the screen.

        This method sets the position of the window so that it is
        centered on the screen. It does this by first getting the
        geometry of the screen and the window, then calculating the
        center point of the screen. Finally, it moves the window to
        be centered at that point.
        """
        screen = QDesktopWidget().screenGeometry()
        window = self.geometry()
        center_point = screen.center()
        self.move(
            center_point.x() - window.width() // 2,
            center_point.y() - window.height() // 2,
        )
