# ZIP Brute Force

A modern GUI application built with PyQt6 and QFluentWidgets for cracking password-protected ZIP files through brute force and dictionary attacks.

## Features

- 🔐 Support for both standard ZIP and AES-encrypted ZIP files
- 📚 Dictionary-based attack using custom wordlists
- 🔄 Brute force attack with customizable character sets
- ⚡ Multi-threaded password attempts
- 🎯 Real-time progress tracking
- 🛑 Ability to stop attacks mid-process
- 🎨 Modern and intuitive user interface

## Requirements

- Python 3.8+
- PyQt6
- PyQt6-FluentWidgets
- pyzipper

## Installation

1. Clone the repository:
```bash
git clone https://github.com/junior-rumiche/zip-brutter.git
cd zip-brutter
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python main.py
```

2. Select a ZIP file to crack
3. Choose between dictionary attack or brute force:
   - For dictionary attack: Select a wordlist file
   - For brute force: Configure character options and password length
4. Click "Start Attack" to begin the cracking process
5. Monitor progress in real-time
6. Use "Stop Attack" to halt the process at any time

## Security Notice

This tool is intended for educational purposes and legitimate password recovery only. Do not use it to access ZIP files without authorization.
