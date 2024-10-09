import os
import json
import base64
import sqlite3
import win32crypt
from Cryptodome.Cipher import AES
import shutil
import random
import tkinter as tk
from tkinter import PhotoImage, messagebox, filedialog

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
    profile_folders = [folder for folder in os.listdir(CHROME_USER_DATA_PATH) if folder.startswith("Profile")]
    passwords = []

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
                        passwords.append((interesting_index, url, username, decrypted_password))
                cursor.close()
                connection.close()
                os.remove("TempLoginVault.db")
            else:
                passwords.append(("[ERR]", f"Unable to retrieve passwords for profile: {profile}", "", ""))
        else:
            passwords.append(("[WARN]", f"Login Data file not found for profile: {profile}", "", ""))
    
    return passwords

def show_passwords():
    passwords = get_chrome_passwords()
    password_text.delete('1.0', tk.END)
    for interesting_index, url, username, decrypted_password in passwords:
        password_text.insert(tk.END, f"{interesting_index}\nURL: {url}\nUsername: {username}\nPassword: {decrypted_password}\n{'*' * 50}\n")

    # Display search functionality only after retrieving passwords
    show_search_functionality()

def clear_passwords():
    password_text.delete('1.0', tk.END)
    hide_search_functionality()

def save_passwords():
    passwords = password_text.get('1.0', tk.END)
    if not passwords.strip():
        messagebox.showwarning("No Passwords", "No passwords to save.")
        return

    # Ask for file location to save
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(passwords)
        messagebox.showinfo("Success", "Passwords saved successfully.")

def search_passwords():
    query = search_entry.get().lower()
    if not query:
        messagebox.showwarning("Empty Search", "Please enter a keyword to search.")
        return

    # Clear any previous highlights
    password_text.tag_remove('highlight', '1.0', tk.END)

    # Get the current text
    content = password_text.get('1.0', tk.END)
    
    # Split into lines for searching
    lines = content.splitlines()
    
    # Search for the query in each line
    found_match = False
    for line_number, line in enumerate(lines):
        start_index = f"{line_number + 1}.0"
        end_index = f"{line_number + 1}.end"
        if query in line.lower():
            password_text.tag_add('highlight', start_index, end_index)
            found_match = True

    # Configure the highlight tag
    password_text.tag_config('highlight', background='yellow')

    # Show message if no matches found
    if not found_match:
        messagebox.showinfo("No Matches", "No matching passwords found.")

# Create and show search functionality
def show_search_functionality():
    global search_frame, search_entry, search_button
    search_frame = tk.Frame(root, bg="#424A63")  # Set the background color of the frame
    search_frame.pack(padx=10, pady=10)

    search_entry = tk.Entry(search_frame, width=40, font=("Arial", 10))
    search_entry.pack(side=tk.LEFT, padx=10)

    search_button = tk.Button(search_frame, text="Search", command=search_passwords, bg="#B0EB83", fg="#060101", padx=10, pady=5)
    search_button.pack(side=tk.LEFT, padx=10)

def hide_search_functionality():
    if 'search_frame' in globals():
        search_frame.pack_forget()  # Remove the search frame from the UI
        search_frame.destroy()  # Destroy the search frame

root = tk.Tk()
root.title("Aqeel's Vault")
root.configure(background="#424A63")  # Set the background color to a dark gray

try:
    icon = PhotoImage(file='vault.png')  # Replace with 'vault.ico' if you converted to ICO
    root.iconphoto(False, icon)
except Exception as e:
    print(f"[ERR] Unable to set icon: {e}")

# Create a frame to hold the buttons
button_frame = tk.Frame(root, bg="#424A63")  # Set the background color of the frame to match the root window
button_frame.pack(padx=10, pady=10)

# Create the buttons
password_button = tk.Button(button_frame, text="Retrieve Secrets", command=show_passwords, bg="#B0EB83", fg="#060101", padx=10, pady=5)
password_button.pack(side=tk.LEFT, padx=10)

clear_button = tk.Button(button_frame, text="Clear Secrets", command=clear_passwords, bg="#F67486", fg="#060101", padx=10, pady=5)
clear_button.pack(side=tk.LEFT, padx=10)

# Save to file button
save_button = tk.Button(button_frame, text="Save to File", command=save_passwords, bg="#FFD700", fg="#060101", padx=10, pady=5)
save_button.pack(side=tk.LEFT, padx=10)

# Create a frame to hold the text box
text_frame = tk.Frame(root, bg="#50576E")  # Set the background color of the frame to match the root window
text_frame.pack(padx=10, pady=10)

# Create the text box
password_text = tk.Text(text_frame, height=20, width=60, font=("Arial", 10), bg="#f0f0f0", fg="#000")
password_text.pack(padx=10, pady=10)

root.mainloop()
