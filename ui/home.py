import subprocess
import sys
import os

import asyncio
import threading
from tkinter import ttk

from ui.utils import center_window
from ui.tabs.map_tab import MapTab

# from ui.tabs.predictive_tab import PredictiveTab
from ui.tabs.notifications_tab import NotificationsTab
from scraper.scraper_agent import run_agent

from nlp_processor import NLPProcessor
from location_validator import LocationValidator
from predictive_model import PredictiveModel


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
        self.nlp = NLPProcessor()
        self.lv = LocationValidator()
        self.pm = PredictiveModel()
        self.pm.initModel()

        # Notebook
        self.tabs = ttk.Notebook(root)
        self.tabs.pack(fill="both", expand=True)

        # Notifications Tab
        if role in ["operator", "manager"]:
            self.notifications_tab = NotificationsTab(
                self.tabs, self.nlp, self.lv, self.email, self.role
            )
            self.tabs.add(self.notifications_tab.frame, text="Notifications")

            # threading.Thread(
            #     target=start_agent, args=(self.notifications_tab.refresh,), daemon=True
            # ).start()

        # Map Tab
        self.map_tab = MapTab(self.tabs, self.email, self.role)
        self.tabs.add(self.map_tab.frame, text="Map View")

        # Predictive Tab
        # if role == "manager":
        #     self.predict_tab = PredictiveTab(self.tabs, self.pm)
        #     self.tabs.add(self.predict_tab.frame, text="Predictive Model")

        self.tabs.bind("<<NotebookTabChanged>>", self.on_tab_change)

    def on_tab_change(self, event):
        # Get the text of the currently selected tab
        selected_tab = self.tabs.tab(self.tabs.select(), "text")

        # Trigger specific refreshes based on the tab name
        if selected_tab == "Map View":
            if hasattr(self, "map_tab"):
                self.map_tab.refresh()
        elif selected_tab == "Notifications":
            if hasattr(self, "notifications_tab"):
                self.notifications_tab.refresh()

    def logout(self):
        if hasattr(self, "map_tab") and hasattr(self.map_tab, "_refresh_id"):
            self.root.after_cancel(self.map_tab._refresh_id)

        self.root.withdraw()

        entry_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "entry.py")
        )

        subprocess.Popen([sys.executable, entry_path])
        self.root.quit()
        self.root.destroy()


def start_agent(callback):
    asyncio.run(run_agent(callback))
