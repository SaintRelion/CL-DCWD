import tkinter as tk
from tkinter import ttk, messagebox
from database.db_users import register_user, username_exists, get_all_users


class UserTab:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg="#f4f7f6")

        # 1. SIDEBAR (Registration Form)
        self.sidebar = tk.Frame(self.frame, width=300, bg="white", bd=1, relief="ridge")
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)
        self.sidebar.pack_propagate(False)

        tk.Label(
            self.sidebar,
            text="ADD NEW USER",
            font=("Arial", 12, "bold"),
            bg="white",
            fg="#2c3e50",
        ).pack(pady=20)

        # Form Fields
        fields_frame = tk.Frame(self.sidebar, bg="white", padx=20)
        fields_frame.pack(fill="both", expand=True)

        # Username
        tk.Label(fields_frame, text="Username", bg="white", font=("Arial", 10)).pack(
            anchor="w"
        )
        self.username_ent = tk.Entry(
            fields_frame, font=("Arial", 11), relief="solid", bd=1
        )
        self.username_ent.pack(fill="x", pady=(0, 15), ipady=5)

        # # Email
        # tk.Label(fields_frame, text="Email", bg="white", font=("Arial", 10)).pack(
        #     anchor="w"
        # )
        # self.email_ent = tk.Entry(
        #     fields_frame, font=("Arial", 11), relief="solid", bd=1
        # )
        # self.email_ent.pack(fill="x", pady=(0, 15), ipady=5)

        # Role Selection (Manager Removed)
        tk.Label(fields_frame, text="Role", bg="white", font=("Arial", 10)).pack(
            anchor="w"
        )
        self.role_var = tk.StringVar()
        self.role_combo = ttk.Combobox(
            fields_frame,
            textvariable=self.role_var,
            values=["operator", "tubero"],
            state="readonly",
        )
        self.role_combo.pack(fill="x", pady=(0, 15), ipady=5)

        # Password Container (To be toggled)
        self.pass_container = tk.Frame(fields_frame, bg="white")
        self.pass_container.pack(fill="x")

        tk.Label(
            self.pass_container, text="Password", bg="white", font=("Arial", 10)
        ).pack(anchor="w")
        self.pass_ent = tk.Entry(
            self.pass_container, font=("Arial", 11), relief="solid", bd=1, show="*"
        )
        self.pass_ent.pack(fill="x", pady=(0, 15), ipady=5)

        # Toggle Logic: Hide password if tubero
        def toggle_password(*args):
            if self.role_var.get() == "tubero":
                self.pass_container.pack_forget()
                self.pass_ent.delete(0, tk.END)
            else:
                self.pass_container.pack(fill="x", after=self.role_combo)

        self.role_var.trace_add("write", toggle_password)
        self.role_combo.current(0)  # Triggers trace

        tk.Button(
            self.sidebar,
            text="REGISTER USER",
            bg="#2ecc71",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.handle_register,
            relief="flat",
            pady=10,
            cursor="hand2",
        ).pack(fill="x", padx=20, pady=20)

        # 2. MAIN CONTENT (User Table)
        self.content = tk.Frame(self.frame, bg="#f4f7f6")
        self.content.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        tk.Label(
            self.content,
            text="USER MANAGEMENT",
            font=("Arial", 12, "bold"),
            bg="#f4f7f6",
        ).pack(anchor="w", pady=(0, 10))

        # Table Styling
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 10), rowheight=30)
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))

        self.tree = ttk.Treeview(
            self.content, columns=("ID", "Username", "Role"), show="headings"
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("Username", text="USERNAME")
        # self.tree.heading("Email", text="EMAIL")
        self.tree.heading("Role", text="ROLE")

        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Role", width=100, anchor="center")
        self.tree.pack(fill="both", expand=True)

        self.refresh_table()

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        users = get_all_users()
        for u in users:
            self.tree.insert("", "end", values=u)

    def handle_register(self):
        u = self.username_ent.get().strip()
        # e = self.email_ent.get().strip()
        r = self.role_var.get()
        # If tubero, password is null/blank; otherwise get from entry
        p = self.pass_ent.get().strip() if r != "tubero" else ""

        if not all([u]) or (r == "operator" and not p):
            messagebox.showwarning("Error", "Required fields are missing")
            return

        if username_exists(u):
            messagebox.showerror("Error", "Username already taken")
            return

        try:
            register_user(u, "", p, r)
            messagebox.showinfo("Success", f"User {u} registered")
            self.username_ent.delete(0, tk.END)
            self.email_ent.delete(0, tk.END)
            self.pass_ent.delete(0, tk.END)
            self.refresh_table()
        except Exception as ex:
            messagebox.showerror("Error", f"Failed: {ex}")
