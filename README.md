# Aqeel's Vault

**Aqeel's Vault** is a post-exploitation tool designed for **Windows** environments, aimed at extracting saved passwords from Google Chrome. The tool decrypts Chrome passwords that are stored locally on a compromised system using the system's encryption key and displays them in a readable format. This tool is useful for gathering credentials after gaining unauthorized access to a Windows machine.

> **Note**: This tool is strictly for educational and ethical use. Only use it on systems where you have explicit permission.

## Features

- Decrypt and display saved passwords from Google Chrome.
- Export decrypted passwords to a text file for further analysis.
- Random interesting phrases displayed with each password to keep the user engaged.
- Supports both **Command-Line Interface (CLI)** and **Graphical User Interface (GUI)** versions for flexibility depending on how you access the system.

## Tool Purpose

This is a **post-exploitation tool** that can be used after gaining unauthorized access to a Windows system to retrieve saved Chrome passwords. Depending on how you access the system:

- **GUI Version**: Use this when you have full access to the system and can operate the GUI.
- **CLI Version**: Use this when you only have access to the Windows terminal or command prompt.

## Limitations

- This tool is intended for use on **Windows** machines where Chrome is installed and passwords are saved locally.
- **Kali Linux**: The tool may not work correctly with Chrome installations on Kali Linux or other Linux-based systems due to differences in how encryption keys are stored and managed.

## Installation (No Git Required)

Since Git is not commonly installed on Windows machines, you can manually download the necessary files and run the tool without needing Git.

### Steps:

1. Download the **Aqeel's Vault** ZIP file from the release page (github page)
2. Unzip the file to a location on your Windows system.
3. Open a **Command Prompt** or **PowerShell** window in the unzipped folder.
4. Install the required Python libraries using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Tool

### Command-Line Interface (CLI) Version

The CLI version is useful if you have access to the terminal or command prompt on the compromised Windows system.

1. Navigate to the directory where Aqeel's Vault is located.
2. Run the tool by typing:
   ```bash
   python cli_version.py
   ```
3. To save the retrieved passwords to a file:
   ```bash
   python cli_version.py --save output.txt
   ```

### Graphical User Interface (GUI) Version

The GUI version is designed for ease of use when you have full access to the Windows machine, including the graphical interface.

1. Open the **Command Prompt** in the directory where Aqeel's Vault is located.
2. Run the GUI version using:
   ```bash
   python gui_version.py
   ```
3. Use the **Retrieve Secrets** button to extract stored passwords. You can also search through the passwords using the search bar.
4. To save the retrieved passwords, click on **Save to File**.


## Credits

This tool is inspired by the article:  
**[How to decrypt Chrome password with Python?](https://medium.com/@yicongli/how-to-decrypt-chrome-password-with-python-4a42ab2a038d)**  
by **Yicong**, published on January 5, 2021.
