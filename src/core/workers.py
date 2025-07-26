from PyQt5.QtCore import QObject, QThread, pyqtSignal
from src.core.attacks import BruteForceAttack, DictionaryAttack
import itertools
import time


class AttackWorker(QObject):
    """
    A worker class that performs ZIP file password cracking operations.
    It runs in a separate thread to keep the GUI responsive.
    """

    finished = pyqtSignal(str)
    progress = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(
        self,
        file_path,
        dict_path=None,
        numbers=True,
        letters=False,
        symbols=False,
        length=4,
        parent=None,
        **kwargs,
    ):
        super(AttackWorker, self).__init__(parent)
        self.running = True
        self.attack = None
        if dict_path:
            self.attack = DictionaryAttack(file_path, dict_path, parent=self)
        else:
            max_workers = kwargs.get("max_workers", 10)
            self.attack = BruteForceAttack(
                file_path, length, numbers, letters, symbols, parent=self, max_workers=max_workers
            )
        self.attack.progress.connect(self.progress)

        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self.run)
        self.finished.connect(self.thread.quit)
        self.finished.connect(self.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

    def stop(self):
        self.running = False
        if self.attack:
            self.attack.stop()
        if self.thread and self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()

    def start(self):
        if not self.thread.isRunning():
            self.thread.start()

    def run(self):
        try:
            password = self.attack.run()
            if password:
                self.finished.emit(f"Password found: {password}")
            elif self.running:
                self.finished.emit("Password not found after all attempts")

        except Exception as e:
            self.error.emit(f"Error during attack: {str(e)}")
