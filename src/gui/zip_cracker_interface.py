from PyQt5.QtCore import QFile, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFileDialog
from qfluentwidgets import (
    Dialog,
    InfoBar,
    InfoBarPosition,
    PushButton,
    LineEdit,
    TextEdit,
    FluentIcon,
    Slider,
    TitleLabel,
    BodyLabel,
    TransparentPushButton,
    SwitchButton,
    IndeterminateProgressBar,
    StrongBodyLabel,
)
from src.core.workers import AttackWorker
from src.widgets.modern_card import ModernCardWidget


class ZipCrackerInterface(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("zipCrackerInterface")
        self.setup_ui()
        self.setup_style()
        self.worker = None

    def closeEvent(self, event):
        """
        Handles the close event for the window.

        This method overrides the default close event to ensure that
        any ongoing password cracking attack is stopped before the
        window is closed. If there is an active worker, it stops the
        attack and then proceeds with the standard close event.

        :param event: The close event to handle.
        """
        if self.worker:
            self.worker.stop()
        super().closeEvent(event)

    def setup_style(self):
        self.setStyleSheet(
            """
            QWidget {
                background-color: transparent;
            }
            TitleLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
            }
            BodyLabel {
                color: rgba(255, 255, 255, 0.8);
                font-size: 14px;
            }
            StrongBodyLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
            LineEdit {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 5px;
                padding: 5px;
                color: white;
            }
            TextEdit {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 5px;
                padding: 5px;
                color: white;
            }
            PushButton {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 5px;
                padding: 8px 16px;
                color: white;
            }
            PushButton:hover {
                background: rgba(255, 255, 255, 0.15);
            }
            SwitchButton {
                color: white;
            }
            SwitchButton:checked {
                color: white;
            }
        """
        )

    def setup_ui(self):
        """
        Sets up the user interface for the ZIP Password Cracker application.

        This method creates and arranges various UI components including
        headers, file selection inputs, password options, action buttons,
        and an output display area. It initializes and configures
        ModernCardWidgets for visual grouping, sets up layout management,
        and connects signals to their respective slots.
        """
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Header
        header_card = ModernCardWidget(self)
        header_layout = QVBoxLayout(header_card)
        header_layout.setSpacing(10)
        header_layout.setContentsMargins(20, 20, 20, 20)

        title = TitleLabel("Zip Brute Force", self)
        title.setFixedHeight(40)
        description = BodyLabel(
            "Brute force attack on password-protected ZIP files", self
        )
        header_layout.addWidget(title)
        header_layout.addWidget(description)
        layout.addWidget(header_card)

        # File selection card
        file_card = ModernCardWidget(self)
        file_layout = QVBoxLayout(file_card)
        file_layout.setSpacing(15)
        file_layout.setContentsMargins(20, 20, 20, 20)

        # ZIP file selection
        zip_title = StrongBodyLabel("ZIP File", self)
        file_layout.addWidget(zip_title)

        zip_layout = QHBoxLayout()
        self.zip_path = LineEdit(self)
        self.zip_path.setPlaceholderText("Select your protected ZIP file")
        self.zip_path.setFixedHeight(36)
        self.pick_file_btn = TransparentPushButton("Select", self)
        self.pick_file_btn.setIcon(FluentIcon.FOLDER)
        self.pick_file_btn.setFixedWidth(100)
        zip_layout.addWidget(self.zip_path)
        zip_layout.addWidget(self.pick_file_btn)
        file_layout.addLayout(zip_layout)

        # Dictionary file selection
        dict_title = StrongBodyLabel("Dictionary", self)
        file_layout.addWidget(dict_title)

        dict_layout = QHBoxLayout()
        self.dict_path = LineEdit(self)
        self.dict_path.setPlaceholderText("Select your dictionary file")
        self.dict_path.setFixedHeight(36)
        self.pick_dict_btn = TransparentPushButton("Select", self)
        self.pick_dict_btn.setIcon(FluentIcon.DOCUMENT)
        self.pick_dict_btn.setFixedWidth(100)
        dict_layout.addWidget(self.dict_path)
        dict_layout.addWidget(self.pick_dict_btn)
        file_layout.addLayout(dict_layout)
        layout.addWidget(file_card)

        # Options card
        options_card = ModernCardWidget(self)
        options_layout = QVBoxLayout(options_card)
        options_layout.setSpacing(15)
        options_layout.setContentsMargins(20, 20, 20, 20)

        options_title = StrongBodyLabel("Password Options", self)
        options_layout.addWidget(options_title)

        # Character switches
        switches_layout = QHBoxLayout()
        self.numbers_switch = SwitchButton("Numbers (0-9)", self)
        self.numbers_switch.setChecked(True)
        self.letters_switch = SwitchButton("Letters (a-zA-Z)", self)
        self.symbols_switch = SwitchButton("Symbols (!@#$)", self)
        switches_layout.addWidget(self.numbers_switch)
        switches_layout.addWidget(self.letters_switch)
        switches_layout.addWidget(self.symbols_switch)
        switches_layout.addStretch()
        options_layout.addLayout(switches_layout)

        # Password length slider
        slider_layout = QVBoxLayout()
        slider_header = QHBoxLayout()
        slider_label = StrongBodyLabel("Password Length:", self)
        self.length_value = BodyLabel("4", self)
        slider_header.addWidget(slider_label)
        slider_header.addWidget(self.length_value)
        slider_layout.addLayout(slider_header)

        self.length_slider = Slider(Qt.Horizontal, self)
        self.length_slider.setRange(1, 20)
        self.length_slider.setValue(4)
        slider_layout.addWidget(self.length_slider)

        options_layout.addLayout(slider_layout)
        layout.addWidget(options_card)

        # Start Attack button and progress
        action_card = ModernCardWidget(self)
        action_layout = QVBoxLayout(action_card)
        action_layout.setContentsMargins(20, 20, 20, 20)

        buttons_layout = QHBoxLayout()
        self.start_btn = PushButton("Start Attack", self)
        self.start_btn.setIcon(FluentIcon.PLAY)
        self.start_btn.setFixedSize(200, 40)

        self.stop_btn = PushButton("Stop Attack", self)
        self.stop_btn.setIcon(FluentIcon.STOP_WATCH)
        self.stop_btn.setFixedSize(200, 40)
        self.stop_btn.setEnabled(False)

        buttons_layout.addWidget(self.start_btn, alignment=Qt.AlignCenter)
        buttons_layout.addWidget(self.stop_btn, alignment=Qt.AlignCenter)

        self.progress_bar = IndeterminateProgressBar(self)
        self.progress_bar.setVisible(False)

        action_layout.addLayout(buttons_layout)
        action_layout.addWidget(self.progress_bar)
        layout.addWidget(action_card)

        # Output card
        output_card = ModernCardWidget(self)
        output_layout = QVBoxLayout(output_card)
        output_layout.setSpacing(10)
        output_layout.setContentsMargins(20, 20, 20, 20)

        output_title = StrongBodyLabel("Results", self)
        output_layout.addWidget(output_title)

        self.output_text = TextEdit(self)
        self.output_text.setPlaceholderText("Attack results will appear here...")
        self.output_text.setFixedHeight(150)
        output_layout.addWidget(self.output_text)
        layout.addWidget(output_card)

        # Connect signals
        self.pick_file_btn.clicked.connect(self.pick_zip_file)
        self.pick_dict_btn.clicked.connect(self.pick_dictionary)
        self.start_btn.clicked.connect(self.start_attack)
        self.stop_btn.clicked.connect(self.stop_attack)
        self.length_slider.valueChanged.connect(self._on_slider_changed)

    def _on_slider_changed(self, value):
        self.length_value.setText(str(value))

    def pick_zip_file(self):
        """
        Opens a file dialog for the user to select a ZIP file.

        The selected file path is stored in the `zip_path` LineEdit.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select ZIP File", "", "ZIP Files (*.zip)"
        )
        if file_path:
            self.zip_path.setText(file_path)
        pass

    def pick_dictionary(self):
        """
        Opens a file dialog for the user to select a dictionary file.

        The selected file path is stored in the `dict_path` LineEdit.
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Dictionary File", "", "Text Files (*.txt)"
        )
        if file_path:
            self.dict_path.setText(file_path)
        pass

    def start_attack(self):
        """
        Initiates the password cracking attack on the selected ZIP file.

        This method checks if a ZIP file is selected and initializes an
        AttackWorker with the selected options for numbers, letters, symbols,
        and password length. It connects the worker's signals to appropriate
        handlers and starts the attack process in a separate thread, updating
        the UI elements accordingly.

        Displays an error message if no ZIP file is selected.
        """
        if not self.zip_path.text():
            InfoBar.error(
                content="Please select a ZIP file",
                title="Error",
                orient=Qt.Vertical,
                position=InfoBarPosition.TOP,
                isClosable=True,
                parent=self,
            )
            return

        if self.worker:
            self.worker.stop()
            self.worker = None

        zip_path = self.zip_path.text()
        dict_path = self.dict_path.text()
        numbers = self.numbers_switch.isChecked()
        letters = self.letters_switch.isChecked()
        symbols = self.symbols_switch.isChecked()
        length = self.length_slider.value()

        self.worker = AttackWorker(
            zip_path, dict_path, numbers, letters, symbols, length
        )
        self.worker.finished.connect(self.worker_finished)
        self.worker.progress.connect(self.worker_progress)
        self.worker.error.connect(self.worker_error)
        self.worker.start()
        self.progress_bar.setVisible(True)
        self.progress_bar.start()
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

    def stop_attack(self):
        """
        Stops the ongoing password cracking attack.

        This method stops the AttackWorker if it is running, resets the
        worker instance to None, stops and hides the progress bar, and
        updates the UI to enable the start button and disable the stop
        button. A message indicating the attack was stopped by the user
        is displayed in the output text area.
        """
        if self.worker:
            self.worker.stop()
            self.worker = None
            self.progress_bar.stop()
            self.progress_bar.setVisible(False)
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.output_text.setText("Attack stopped by user")

    def worker_finished(self, message):
        """
        Handles the completion of the password cracking attack.

        This method is called when the AttackWorker emits the 'finished' signal.
        It stops and hides the progress bar, updates the output text with the
        provided message, enables the start button, and disables the stop button.
        If there is an active worker, it stops and resets it.

        Additionally, it displays a dialog with the result message.

        :param message: The result message to display in the output text and dialog.
        """
        self.progress_bar.stop()
        self.progress_bar.setVisible(False)
        self.output_text.setText(message)
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        if self.worker:
            self.worker.stop()
            self.worker = None

        w = Dialog("Information", message, self)
        w.exec_()

    def worker_progress(self, message):
        """
        Updates the output text with the latest progress message from the AttackWorker.

        This method is called when the AttackWorker emits the 'progress' signal.
        It sets the text of the output text area to the provided message.

        :param message: The progress message to display in the output text.
        """
        self.output_text.setText(message)

    def worker_error(self, message):
        """
        Handles errors that occur during the password cracking attack.

        This method is called when the AttackWorker emits the 'error' signal.
        It stops and hides the progress bar, updates the output text with the
        provided error message, enables the start button, and disables the stop
        button. If there is an active worker, it stops and resets it.

        :param message: The error message to display in the output text.
        """
        self.progress_bar.stop()
        self.progress_bar.setVisible(False)
        self.output_text.setText(f"Error: {message}")
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        if self.worker:
            self.worker.stop()
            self.worker = None
