import string
import itertools
import pyzipper
from abc import ABC, abstractmethod
from PyQt5.QtCore import QObject, pyqtSignal
from abc import ABCMeta

class CombinedMeta(type(QObject), ABCMeta):
    pass

class Attack(QObject, ABC, metaclass=CombinedMeta):
    """
    Abstract base class for different attack strategies.
    """
    progress = pyqtSignal(str)

    def __init__(self, file_path, parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.running = True

    @abstractmethod
    def run(self):
        pass

    def stop(self):
        self.running = False

    def try_password(self, password):
        """
        Attempt to extract the ZIP file using the provided password.
        """
        encoded_pwd = password.encode()
        try:
            with pyzipper.ZipFile(self.file_path) as zip_file:
                zip_file.extractall(pwd=encoded_pwd)
            return True
        except Exception:
            try:
                with pyzipper.AESZipFile(self.file_path) as zip_file:
                    zip_file.extractall(pwd=encoded_pwd)
                return True
            except Exception:
                return False


class DictionaryAttack(Attack):
    """
    Performs a dictionary-based attack on a ZIP file.
    """

    def __init__(self, file_path, dict_path, parent=None):
        super().__init__(file_path, parent)
        self.dict_path = dict_path

    def run(self):
        total_attempts = 0
        with open(self.dict_path, "r", encoding="utf-8", errors="ignore") as password_file:
            for password in password_file:
                if not self.running:
                    return None
                password = password.strip()
                total_attempts += 1
                if total_attempts % 10 == 0:
                    self.progress.emit(
                        f"Trying password: {password} (Attempts: {total_attempts})"
                    )
                if self.try_password(password):
                    return password
        return None


from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time
import sys


class BruteForceAttack(Attack):
    """
    Performs a parallelized brute-force attack on a ZIP file.

    This class uses a ThreadPoolExecutor to test multiple passwords concurrently,
    significantly speeding up the brute-force process.

    Attributes:
        length (int): The maximum password length to check.
        numbers (bool): Whether to include numbers in the character set.
        letters (bool): Whether to include letters in the character set.
        symbols (bool): Whether to include symbols in the character set.
        password_found (str): The correct password, if found.
        stop_event (threading.Event): An event to signal all threads to stop.
        total_attempts (int): A counter for the number of passwords tried.
    """

    def __init__(self, file_path, length, numbers, letters, symbols, parent=None):
        super().__init__(file_path, parent)
        self.length = length
        self.numbers = numbers
        self.letters = letters
        self.symbols = symbols
        self.password_found = None
        self.stop_event = threading.Event()
        self.total_attempts = 0

    def __get_combinations(self):
        """
        Generates the character set for the brute-force attack.

        Returns:
            str: A string containing all characters to be used in the attack.
        """
        combinations = ""
        if self.numbers:
            combinations += string.digits
        if self.letters:
            combinations += string.ascii_letters
        if self.symbols:
            combinations += string.punctuation
        return combinations if combinations else string.digits

    def _check_password(self, password):
        """
        Checks a single password against the ZIP file.

        This method is designed to be called from a worker thread. It stops
        early if the stop_event is set by another thread.

        Args:
            password (str): The password to try.

        Returns:
            str or None: The password if it's correct, otherwise None.
        """
        if self.stop_event.is_set():
            return None

        self.total_attempts += 1
        if self.total_attempts % 1000 == 0:
            # Log progress to the console, overwriting the previous line
            sys.stdout.write(f"\rTrying password: {password} (Attempts: {self.total_attempts})")
            sys.stdout.flush()

        if self.try_password(password):
            self.stop_event.set()
            return password
        return None

    def run(self):
        combinations = self.__get_combinations()
        with ThreadPoolExecutor(max_workers=10) as executor:
            for length in range(1, self.length + 1):
                if self.stop_event.is_set():
                    break

                passwords = (
                    "".join(p)
                    for p in itertools.product(combinations, repeat=length)
                )

                # Process passwords in batches
                while True:
                    if self.stop_event.is_set():
                        break

                    batch = list(itertools.islice(passwords, 10000))
                    if not batch:
                        break

                    futures = {executor.submit(self._check_password, p) for p in batch}

                    for future in as_completed(futures):
                        result = future.result()
                        if result:
                            self.password_found = result
                            # Cancel remaining futures
                            for f in futures:
                                if not f.done():
                                    f.cancel()
                            return self.password_found
        return None
