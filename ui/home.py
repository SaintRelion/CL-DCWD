import subprocess
import sys
import os

import asyncio
import threading
from tkinter import ttk

from ui.tabs.user_tab import UserTab
from ui.utils import center_window
from ui.tabs.map_tab import MapTab

from ui.tabs.predictive_tab import PredictiveTab
from ui.tabs.notifications_tab import NotificationsTab
from scraper.scraper_agent import run_agent

from ai.location_validator import LocationValidator

from ai.predictive_model import PredictiveModel


class App:
    def __init__(self, root, username, email, role):

        self.root = root
        self.username = username
        self.email = email
        self.role = role

        self.root.title("DCWD Incident Monitoring System")
        center_window(self.root, 1200, 700)

        # Top bar
        topbar = ttk.Frame(root)
        topbar.pack(fill="x")

        ttk.Label(
            topbar,
            text=f"Logged in as: {username} ({role})",
            font=("Segoe UI", 10, "bold"),
        ).pack(side="right", padx=10, pady=5)

        ttk.Button(topbar, text="Logout", command=self.logout).pack(
            side="right", padx=10
        )

        # Initialize modules
        self.lv = LocationValidator()
        self.pm = PredictiveModel()

        # FIX: Move heavy ML loading off the main thread to stop initial lag
        threading.Thread(target=self._load_predictive_models, daemon=True).start()

        # Notebook
        self.tabs = ttk.Notebook(root)
        self.tabs.pack(fill="both", expand=True)

        # User Tab
        if self.role == "manager":
            self.user_tab = UserTab(self.tabs)
            self.tabs.add(self.user_tab.frame, text="User Management")

        # Notifications Tab
        if role == "operator":
            self.notifications_tab = NotificationsTab(
                self.tabs, self.lv, self.email, self.role
            )
            self.tabs.add(self.notifications_tab.frame, text="Notifications")

            # threading.Thread(
            #     target=start_agent, args=(self.notifications_tab.refresh,), daemon=True
            # ).start()

        # Map Tab
        self.map_tab = MapTab(self.tabs, self.email, self.role)
        self.tabs.add(self.map_tab.frame, text="Map View")

        # Predictive Tab
        self.predict_tab = PredictiveTab(self.tabs, self.pm)
        self.tabs.add(self.predict_tab.frame, text="Predictive Model")

        self.tabs.bind("<<NotebookTabChanged>>", self.on_tab_change)

    def _load_predictive_models(self):
        """Loads machine learning models in the background."""
        try:
            self.pm.initModel()
            # Safely refresh the UI once loaded
            if hasattr(self, "predict_tab"):
                self.root.after(0, self.predict_tab.refresh_view)
        except Exception as e:
            print(f"Error loading predictive models: {e}")

    def on_tab_change(self, event):
        # FIX: Add a safety check to ensure the notebook hasn't been destroyed
        if not self.tabs.winfo_exists():
            return

        try:
            # Check if there are any tabs selected to prevent 'Invalid slave specification'
            selected_id = self.tabs.select()
            if not selected_id:
                return

            selected_tab = self.tabs.tab(selected_id, "text")

            if selected_tab == "Map View":
                if hasattr(self, "map_tab"):
                    self.map_tab.refresh()
            elif selected_tab == "Notifications":
                if hasattr(self, "notifications_tab"):
                    self.notifications_tab.refresh()
        except tk.TclError:
            # Catch trailing Tkinter errors that occur mid-destruction
            pass

    def logout(self):
        self.root.withdraw()

        entry_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "entry.py")
        )
        subprocess.Popen([sys.executable, entry_path])

        os._exit(0)


def start_agent(callback):
    asyncio.run(run_agent(callback))
