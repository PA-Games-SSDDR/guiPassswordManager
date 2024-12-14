import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import messagebox
import os
from cryptography.fernet import Fernet
from store import Storage
from cryptfuncs import hash_password,\
                       generate_password,\
                       verify_password,\
                       password_encrypt,\
                       password_decrypt


# File to store passwords and encryption key
MASTER_PASSWORD = ""
storage = Storage("apasswords.json")
basedir = os.path.dirname(__file__)


# Logout function
def logout():
    main_frame.pack_forget()
    global MASTER_PASSWORD
    MASTER_PASSWORD = ""
    # main_frame.destroy()
    login_frame.pack()


# Login function
def login():
    global MASTER_PASSWORD
    entered_password = master_password_var.get()
    master_password_stored_var = storage.get_master_password()
    if master_password_stored_var is None:
        # first time
        storage.set_master_password(hash_password(entered_password))
        master_password_var.set("")
        login_frame.pack_forget()
        MASTER_PASSWORD = entered_password
        main_frame.pack()
    else:
        if verify_password(master_password_stored_var, entered_password):
            master_password_var.set("")
            login_frame.pack_forget()
            MASTER_PASSWORD = entered_password
            # login_frame.destroy()
            main_frame.pack()
        else:
            messagebox.showerror("Error", "Incorrect master password!")


def refresh_passwords():
    for item in tree.get_children():
        tree.delete(item)

    for password in storage.get_passwords():
        tree.insert('', tk.END, values=(password['service'], password['username']))


def show_add_dialog():
    main_frame.top = tk.Toplevel()
    main_frame.top.iconbitmap(os.path.join(basedir, "icons", "Gui.ico"))
    main_frame.top.title("Add Password")
    main_frame.top.transient(main_frame)
    main_frame.top.minsize(300, 400)
    # Service
    top_service_label = ttk.Label(main_frame.top, text="Service:").pack(padx=5, pady=5)
    top_service_var = tk.StringVar()
    top_service_entry = ttk.Entry(main_frame.top, textvariable=top_service_var).pack(fill=tk.X, padx=5)

    # Username
    top_username_label = ttk.Label(main_frame.top, text="Username:").pack(padx=5, pady=5)
    top_username_var = tk.StringVar()
    top_username_entry = ttk.Entry(main_frame.top, textvariable=top_username_var).pack(fill=tk.X, padx=5)

    # Password
    top_password_label = ttk.Label(main_frame.top, text="Password:").pack(padx=5, pady=5)
    top_password_var = tk.StringVar()
    top_password_entry = ttk.Entry(main_frame.top, textvariable=top_password_var, show="*").pack(fill=tk.X, padx=5)

    # comment
    top_comment_label = ttk.Label(main_frame.top, text="Comment:").pack(padx=5, pady=5)
    top_comment_var = tk.StringVar()
    top_comment_entry = ttk.Entry(main_frame.top, textvariable=top_comment_var).pack(fill=tk.X, padx=5)

    def toggle_password_entry():
        if top_generate_var.get():
            top_password_var.set("")
            top_length_frame.pack(padx=5, pady=5)
        else:
            top_length_frame.pack_forget()

    # Generate password
    top_generate_var = tk.BooleanVar()
    top_checkbutton = ttk.Checkbutton(
        main_frame.top,
        text="Generate password",
        variable=top_generate_var,
        command=toggle_password_entry
    ).pack(padx=5, pady=5)

    # Password length
    top_length_frame = ttk.Frame(main_frame.top)
    top_length_label = ttk.Label(top_length_frame, text="Length:").pack(side=tk.LEFT, padx=5)
    top_length_var = tk.StringVar(value="16")
    top_length_entry = ttk.Entry(top_length_frame, textvariable=top_length_var, width=5).pack(side=tk.LEFT)

    # Buttons
    top_button_frame = ttk.Frame(main_frame.top)
    top_button_frame.pack(fill=tk.X, padx=5, pady=10)

    def save():
        service = top_service_var.get().strip()
        username = top_username_var.get().strip()
        comment = top_comment_var.get().strip()

        if not service or not username:
            messagebox.showerror("Error", "Service and username are required!")

        if top_generate_var.get():
            try:
                length = int(top_length_var.get())
                if length < 8:
                    raise ValueError("Password length must be at least 8")
                password = generate_password(length)
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        else:
            password = top_password_var.get()
            if not password:
                messagebox.showerror("Error", "Password is required!")

        storage.add_password(service, username, password, MASTER_PASSWORD, comment)
        refresh_passwords()
        main_frame.top.destroy()

    top_save_button = ttk.Button(top_button_frame, text="Save", command=save).pack(side=tk.LEFT, padx=5)
    top_cancel_button = ttk.Button(top_button_frame, text="Cancel", command=main_frame.top.destroy).pack(side=tk.RIGHT, padx=5)
    main_frame.top.mainloop()


def show_view_dialog():
    selection = tree.selection()
    if not selection:
        messagebox.showwarning("Warning", "Please select a password to view.")
    else:
        item = tree.item(selection[0])
        service, username = item['values']
        main_frame.topview = tk.Toplevel()
        main_frame.topview.iconbitmap(os.path.join(basedir, "icons", "Gui.ico"))
        main_frame.topview.title("View Password")
        main_frame.topview.transient(main_frame)
        main_frame.topview.minsize(300, 400)
        main_frame.topview.resizable(False, False)
        # Find password
        passwords = storage.get_passwords()
        password_entry = next(
            (p for p in passwords
                if p['service'] == service and p['username'] == username),
            None
        )

        if not password_entry:
            messagebox.showerror("Error", "Password not found!")
            main_frame.topview.destroy()

        # Display details
        topview_service = ttk.Label(main_frame.topview, text=f"Service: {service}").pack(padx=5, pady=5)
        topview_username = ttk.Label(main_frame.topview, text=f"Username: {username}").pack(padx=5, pady=5)
        commenty = password_decrypt(password_entry['comments'], MASTER_PASSWORD).decode('utf-8')
        topview_comment = ttk.Label(main_frame.topview, text=f"Comment: {commenty}").pack(padx=5, pady=5)

        topview_password_frame = ttk.Frame(main_frame.topview)
        topview_password_frame.pack(fill=tk.X, padx=5, pady=5)

        topview_password_var = tk.StringVar(value=password_decrypt(password_entry['password'],
                                                                MASTER_PASSWORD).decode('utf-8'))
        topview_show_password = tk.BooleanVar()

        topview_password_entry = ttk.Entry(
            topview_password_frame,
            textvariable=topview_password_var,
            show="*",
            state="readonly"
        )
        topview_password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Checkbutton(
            topview_password_frame,
            text="Show",
            variable=topview_show_password,
            command=lambda: toggle_password_visibility(topview_password_entry)
        ).pack(side=tk.LEFT, padx=5)

        topview_close_button = ttk.Button(main_frame.topview, text="Close", command=main_frame.topview.destroy).pack(pady=10)

        def toggle_password_visibility(entry):
            entry.configure(show="" if topview_show_password.get() else "*")
        main_frame.topview.mainloop()


def delete_password():
    selection = tree.selection()
    if not selection:
        messagebox.showwarning("Warning", "Please select a password to delete.")
    else:
        item = tree.item(selection[0])
        service, username = item['values']

        if messagebox.askyesno("Confirm", f"Delete password for {service} ({username})?"):
            storage.delete_password(service, username)
            refresh_passwords()


# Create the main application window
root = tk.Tk()
root.title("Password Manager")

# Login Frame
login_frame = ttk.Frame(root)
login_frame.pack()

login_label = tk.Label(login_frame, text="Enter Master Password:")
login_label.grid(row=0, column=0, padx=10, pady=5)
master_password_var = tk.StringVar()
master_password_entry = tk.Entry(login_frame, textvariable=master_password_var, width=30, show="*")
master_password_entry.grid(row=0, column=1, padx=10, pady=5)

login_button = tk.Button(login_frame, text="Login", command=login)
login_button.grid(row=1, column=0, columnspan=2, pady=10)

# Main Frame
main_frame = ttk.Frame(root)
root.iconbitmap(os.path.join(basedir, "icons", "Gui.ico"))
# Main frame - Toolbar
toolbar = ttk.Frame(main_frame)
toolbar.pack(fill=tk.X, padx=5, pady=5)
add_button = ttk.Button(toolbar, text="Add Password", command=show_add_dialog).pack(side=tk.LEFT, padx=5)
view_button = ttk.Button(toolbar, text="View Password", command=show_view_dialog).pack(side=tk.LEFT, padx=5)
delete_button = ttk.Button(toolbar, text="Delete Password", command=delete_password).pack(side=tk.LEFT, padx=5)
logout_button = ttk.Button(toolbar, text="Logout", command=logout).pack(side=tk.RIGHT, padx=5)

# Main Frame - Password list
list_frame = ttk.Frame(main_frame)
list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

columns = ('service', 'username')
tree = ttk.Treeview(list_frame, columns=columns, show='headings')

tree.heading('service', text='Service')
tree.heading('username', text='Username')

scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
refresh_passwords()


tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Start the application
root.iconbitmap(os.path.join(basedir, "icons", "Gui.ico"))
root.mainloop()
