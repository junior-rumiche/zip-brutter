from PyQt5.QtCore import QObject, QThread, pyqtSignal
import itertools
import pyzipper
import time
import string


class AttackWorker(QObject):
    """
    A worker class that performs ZIP file password cracking operations.

    This worker can perform both dictionary-based attacks and brute force attacks
    on password-protected ZIP files. It runs in a separate thread to keep the GUI responsive.

    Signals:
        finished (str): Emitted when the attack is completed, contains result message
        progress (str): Emitted to update on current progress
        error (str): Emitted when an error occurs during the attack
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
    ):
        """
        Initialize an AttackWorker object.

        :param file_path: The path to the ZIP file to crack.
        :param dict_path: The path to the password dictionary file.
        :param numbers: Whether to use numbers in the password (default: True).
        :param letters: Whether to use letters in the password (default: False).
        :param symbols: Whether to use symbols in the password (default: False).
        :param length: The length of the password to generate (default: 4).
        :param parent: The parent QObject (default: None).
        """
        super(AttackWorker, self).__init__(parent)
        self.running = True
        self.file_path = file_path
        self.dict_path = dict_path
        self.numbers = numbers
        self.letters = letters
        self.symbols = symbols
        self.length = length
        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self.run)
        self.finished.connect(self.thread.quit)
        self.finished.connect(self.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

    def stop(self):
        """
        Stop the running thread.

        This method is used to stop the attack process. It will stop the thread that
        is running the attack and wait for it to finish before returning.
        """
        self.running = False
        if self.thread and self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()

    def start(self):
        """
        Start the thread that runs the attack.

        This method is used to start the attack process in a separate thread.
        """
        if not self.thread.isRunning():
            self.thread.start()

    def run(self):
        """
        Main execution method.

        This method starts the attack process in a separate thread.
        """
        try:
            if self.dict_path:
                self.__attack_with_dictionary()
            else:
                self.__attack_with_brute_force()
        except Exception as e:
            self.error.emit(f"Error during attack: {str(e)}")
        finally:
            self.stop()

    def __get_combinations(self):
        """
        Generate the character set for brute force attack.

        This method generates a string containing the characters that can be used
        to generate passwords based on the options selected by the user, such as
        using numbers, letters, and symbols.

        :return: A string containing the characters that can be used to generate
        passwords.
        """
        combinations = ""
        if self.numbers:
            combinations += string.digits
        if self.letters:
            combinations += string.ascii_letters
        if self.symbols:
            combinations += string.punctuation
        return combinations if combinations else string.digits

    def __try_password(self, password):
        """
        Attempt to extract the ZIP file using the provided password.

        This method tries to open the ZIP file with both standard and AES encryption
        methods using the given password. If successful, it emits a 'finished' signal
        with the found password.

        :param password: The password to try for extracting the ZIP file.
        :return: True if the password is correct, False otherwise.
        """
        encoded_pwd = password.encode()

        try:
            with pyzipper.ZipFile(self.file_path) as zip_file:
                zip_file.extractall(pwd=encoded_pwd)
                self.finished.emit(f"Password found: {password}")
                return True
        except:
            pass

        try:
            with pyzipper.AESZipFile(self.file_path) as zip_file:
                zip_file.extractall(pwd=encoded_pwd)
                self.finished.emit(f"Password found: {password}")
                return True
        except:
            return False

    def __attack_with_brute_force(self):
        """
        Perform a brute force attack on the ZIP file.

        This method generates all possible passwords of given length
        (up to the specified maximum length) using the character set
        specified in the constructor and tries each generated password
        against the ZIP file.

        If the password is found, the method will stop and emit the
        "finished" signal with the password as the argument.

        If any errors occur during the attack, the method will emit the
        "error" signal with a descriptive error message as the argument.

        If the attack is stopped by calling the stop() method, the method
        will emit the "finished" signal with the message "Password not found
        after all attempts".

        :return: None
        """
        combinations = self.__get_combinations()
        total_attempts = 0

        for length in range(1, self.length + 1):
            if not self.running:
                break

            for password in itertools.product(combinations, repeat=length):
                if not self.running:
                    break

                password = "".join(password)
                total_attempts += 1

                if total_attempts % 10 == 0:
                    self.progress.emit(
                        f"Trying password: {password} (Attempts: {total_attempts})"
                    )

                if self.__try_password(password):
                    return

                time.sleep(0.01)

        if self.running:
            self.finished.emit("Password not found after all attempts")

    def __attack_with_dictionary(self):
        """
        Perform a dictionary attack on the ZIP file.

        This method reads through a text file line by line, and tries each
        line as a password against the ZIP file. The file should contain
        one password per line.

        If the password is found, the method will stop and emit the
        "finished" signal with the password as the argument.

        If any errors occur during the attack, the method will emit the
        "error" signal with a descriptive error message as the argument.

        :return: None
        """
        try:
            total_attempts = 0
            with open(
                self.dict_path, "r", encoding="utf-8", errors="ignore"
            ) as password_file:
                for password in password_file:
                    if not self.running:
                        break

                    password = password.strip()
                    total_attempts += 1

                    if total_attempts % 10 == 0:
                        self.progress.emit(
                            f"Trying password: {password} (Attempts: {total_attempts})"
                        )

                    if self.__try_password(password):
                        return

                    time.sleep(0.01)

        except Exception as e:
            self.error.emit(f"Dictionary attack error: {str(e)}")
            return
