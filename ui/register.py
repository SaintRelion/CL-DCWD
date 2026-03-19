import tkinter as tk
from tkinter import ttk, messagebox

from ui.utils import center_window
from database.db_users import register_user, username_exists


class RegisterWindow:

    def __init__(self, parent):
        self.parent = parent

        self.window = tk.Toplevel(parent)
        self.window.title("Register User")
        center_window(self.window, 400, 350)
        self.window.resizable(False, False)

        frame = ttk.Frame(self.window, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Create User", font=("Segoe UI", 14, "bold")).pack(
            pady=10
        )

        # Username
        ttk.Label(frame, text="Username").pack(anchor="w")
        self.username = ttk.Entry(frame)
        self.username.pack(fill="x", pady=5)

        # Email
        ttk.Label(frame, text="Email").pack(anchor="w")
        self.email = ttk.Entry(frame)
        self.email.pack(fill="x", pady=5)

        # Password
        ttk.Label(frame, text="Password").pack(anchor="w")
        self.password = ttk.Entry(frame, show="*")
        self.password.pack(fill="x", pady=5)

        # Role
        # TODO: Removed tubero for now
        ttk.Label(frame, text="Role").pack(anchor="w")
        self.role = ttk.Combobox(frame, values=["operator", "tubero"], state="readonly")
        self.role.current(0)
        self.role.pack(fill="x", pady=5)

        ttk.Button(frame, text="Register", command=self.register).pack(pady=15)

    def register(self):

        username = self.username.get()
        email = self.email.get()
        password = self.password.get()
        role = self.role.get()

        if username == "" or email == "" or password == "":
            messagebox.showerror("Error", "Please fill all fields")
            return

        if username_exists(username):
            messagebox.showerror("Error", "Username already exists")
            return

        register_user(username, email, password, role)

        messagebox.showinfo("Success", "User created successfully")
        self.window.destroy()
