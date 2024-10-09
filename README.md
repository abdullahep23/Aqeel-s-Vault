# Aqeel's Vault

**Aqeel's Vault** is a Python-based tool designed to retrieve saved passwords from Google Chrome, decrypt them, and display them in an easy-to-read format. It uses Chrome's encryption key and AES cryptography to decrypt the passwords that Chrome saves in an SQLite database. This tool allows users to see all stored passwords and export them to a text file if desired.

## Description

It is undeniable that saving your passwords in Chrome is convenient. It helps you log in to websites automatically while ensuring that your passwords are encrypted. The only way for perpetrators to access your encrypted website passwords is to have your laptop username and password.

However, while Chrome makes it easy to auto-fill login forms, this creates a false sense of security. Chrome saves these passwords elsewhere in the application, in a location that is not always as secure as you might think.

## Key Features:

- Decrypts saved Chrome passwords.
- Displays passwords along with associated URLs and usernames.
- Provides an option to export decrypted passwords to a text file.
- Offers search functionality to filter results within the tool.

## Requirements

Make sure you have Python installed on your machine. To install the required packages, you can use `pip` to install the dependencies listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```
## Installation
Clone the Repository
Clone the tool repository to your local machine using Git:
```bash
git clone https://github.com/your-repo/aqeels-vault.git
cd aqeels-vault
```
## Install Dependencies
```bash
pip install -r requirements.txt
```
## Running the Tool
## For Command-Line Interface (CLI) Version:
You can run the CLI version by using the following command:
```bash
python cli_version.py
```
Optionally, you can save the retrieved passwords to a text file:
```bash
python cli_version.py --save output.txt
```
For Graphical User Interface (GUI) Version:
Run the following command to open the GUI interface:
```bash
python gui_version.py
```
Use the Retrieve Secrets button to display all stored passwords.
You can search through the displayed passwords using the search bar that appears after retrieving the passwords.
If you want to save the passwords to a text file, click the Save to File button.
