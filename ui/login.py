import tkinter as tk
from tkinter import ttk, messagebox

from ui.utils import center_window
from ui.home import App
from ui.register import RegisterWindow
from database.db_users import get_user


class LoginWindow:

    def __init__(self, root):

        self.root = root
        self.root.title("DCWD Incident Monitoring System")
        center_window(self.root, 400, 300)
        self.root.resizable(False, False)

        main = ttk.Frame(root, padding=30)
        main.pack(fill="both", expand=True)

        ttk.Label(
            main, text="DCWD Incident Monitoring System", font=("Segoe UI", 14, "bold")
        ).pack(pady=10)

        ttk.Label(main, text="Username").pack(anchor="w")
        self.username = ttk.Entry(main)
        self.username.pack(fill="x", pady=5)

        ttk.Label(main, text="Password").pack(anchor="w")
        self.password = ttk.Entry(main, show="*")
        self.password.pack(fill="x", pady=5)

        ttk.Button(main, text="Login", command=self.login).pack(pady=10)

        ttk.Separator(main).pack(fill="x", pady=10)

        ttk.Button(main, text="Register New User", command=self.open_register).pack()

    def login(self):

        username = self.username.get()
        password = self.password.get()

        user = get_user(username, password)

        if user:

            id, username, email, role = user

            self.root.destroy()

            import tkinter as tk

            main_root = tk.Tk()

            App(main_root, username, email, role)

            main_root.mainloop()

        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    def open_register(self):

        RegisterWindow(self.root)
