# Zip Cracker

Zip Cracker is a Python application with a graphical user interface (GUI) for cracking password-protected ZIP files. It supports both dictionary and brute-force attacks. The application is built using PyQt5 and QFluentWidgets for a modern user interface.

## Features

-   **Dictionary Attack**: Crack ZIP files using a wordlist.
-   **Brute-Force Attack**: Systematically try all possible password combinations.
-   **Parallel Processing**: The brute-force attack is optimized to use multiple CPU cores for faster cracking.
-   **User-Friendly Interface**: An intuitive and modern GUI allows you to easily select files and configure attack options.
-   **Responsive**: The cracking process runs in a separate thread to keep the UI responsive.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/junior-rumiche/zip-brutter.git
    cd zip-brutter
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the application:**

    ```bash
    python main.py
    ```

2.  **Select the ZIP file** you want to crack.

3.  **Choose an attack method:**
    -   **For a dictionary attack:** Select a dictionary file (a text file with one password per line).
    -   **For a brute-force attack:** Configure the password length and character sets (numbers, letters, symbols).

4.  **Click "Start Attack"** to begin the cracking process.

5.  The results of the attack will be displayed in the output area.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue.
