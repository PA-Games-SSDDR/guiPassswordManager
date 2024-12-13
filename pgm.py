import tkinter as tk
from tkinter import messagebox
import json
from cryptography.fernet import Fernet

# File to store passwords and encryption key
DATA_FILE = "passwords.json"
KEY_FILE = "key.key"
MASTER_PASSWORD_FILE = "master_password.key"

# Function to load or generate the encryption key
def load_key():
    try:
        with open(KEY_FILE, "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
        return key

# Load the encryption key
KEY = load_key()
fernet = Fernet(KEY)

# Encrypt data
def encrypt(data):
    return fernet.encrypt(data.encode()).decode()

# Decrypt data
def decrypt(data):
    try:
        return fernet.decrypt(data.encode()).decode()
    except Exception:
        return None

# Load or set master password
def load_or_set_master_password(master_password="default_master_password"):
    try:
        with open(MASTER_PASSWORD_FILE, "rb") as master_file:
            return master_file.read().decode()
    except FileNotFoundError:
        # master_password = "default_master_password"
        encrypted_master_password = encrypt(master_password)
        with open(MASTER_PASSWORD_FILE, "wb") as master_file:
            master_file.write(encrypted_master_password.encode())
        return encrypted_master_password


# Load passwords from file
def load_passwords():
    try:
        with open(DATA_FILE, "r") as file:
            encrypted_data = file.read()
            if encrypted_data:
                decrypted_data = decrypt(encrypted_data)
                return json.loads(decrypted_data) if decrypted_data else {}
            return {}
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

# Save passwords to file
def save_passwords(passwords):
    encrypted_data = encrypt(json.dumps(passwords))
    with open(DATA_FILE, "w") as file:
        file.write(encrypted_data)

# Add a new password
def add_password():
    site = site_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if not site or not username or not password:
        messagebox.showerror("Error", "All fields are required!")
        return

    passwords = load_passwords()
    passwords[site] = {"username": username, "password": password}
    save_passwords(passwords)

    messagebox.showinfo("Success", f"Password for {site} added!")
    site_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

# Search for a password
def search_password():
    site = site_entry.get()

    if not site:
        messagebox.showerror("Error", "Please enter a site name to search!")
        return

    passwords = load_passwords()
    if site in passwords:
        username = passwords[site]["username"]
        password = passwords[site]["password"]
        messagebox.showinfo("Found", f"Username: {username}\nPassword: {password}")
    else:
        messagebox.showerror("Not Found", f"No details for {site} found.")

# View all stored passwords
def view_passwords():
    passwords = load_passwords()
    if not passwords:
        messagebox.showinfo("Empty", "No passwords stored.")
        return

    passwords_list = "\n".join(
        [f"{site}: {data['username']} | {data['password']}" for site, data in passwords.items()]
    )
    password_window = tk.Toplevel()
    password_window.title("Stored Passwords")
    text_area = tk.Text(password_window, wrap=tk.WORD, width=50, height=15)
    text_area.insert(tk.END, passwords_list)
    text_area.config(state=tk.DISABLED)
    text_area.pack(padx=10, pady=10)

# Logout function
def logout():
    main_frame.pack_forget()
    login_frame.pack()

# Login function
def login():
    entered_password = master_password_var.get()
    MASTER_PASSWORD = load_or_set_master_password(entered_password)
    if entered_password == decrypt(MASTER_PASSWORD):
        login_frame.pack_forget()
        main_frame.pack()
    else:
        messagebox.showerror("Error", "Incorrect master password!")

# Create the main application window
root = tk.Tk()
root.title("Password Manager")

# Login Frame
login_frame = tk.Frame(root)
login_frame.pack()

login_label = tk.Label(login_frame, text="Enter Master Password:")
login_label.grid(row=0, column=0, padx=10, pady=5)
master_password_var = tk.StringVar()
master_password_entry = tk.Entry(login_frame, textvariable=master_password_var, width=30, show="*")
master_password_entry.grid(row=0, column=1, padx=10, pady=5)

login_button = tk.Button(login_frame, text="Login", command=login)
login_button.grid(row=1, column=0, columnspan=2, pady=10)

# Main Frame
main_frame = tk.Frame(root)

# Labels and entries
site_label = tk.Label(main_frame, text="Website:")
site_label.grid(row=0, column=0, padx=10, pady=5)
site_entry = tk.Entry(main_frame, width=30)
site_entry.grid(row=0, column=1, padx=10, pady=5)

username_label = tk.Label(main_frame, text="Username:")
username_label.grid(row=1, column=0, padx=10, pady=5)
username_entry = tk.Entry(main_frame, width=30)
username_entry.grid(row=1, column=1, padx=10, pady=5)

password_label = tk.Label(main_frame, text="Password:")
password_label.grid(row=2, column=0, padx=10, pady=5)
password_entry = tk.Entry(main_frame, width=30, show="*")
password_entry.grid(row=2, column=1, padx=10, pady=5)

# Buttons
add_button = tk.Button(main_frame, text="Add Password", command=add_password)
add_button.grid(row=3, column=0, columnspan=2, pady=5)

search_button = tk.Button(main_frame, text="Search Password", command=search_password)
search_button.grid(row=4, column=0, columnspan=2, pady=5)

view_button = tk.Button(main_frame, text="View All Passwords", command=view_passwords)
view_button.grid(row=5, column=0, columnspan=2, pady=5)

logout_button = tk.Button(main_frame, text="Logout", command=logout)
logout_button.grid(row=6, column=0, columnspan=2, pady=5)

# Start the application
root.mainloop()
