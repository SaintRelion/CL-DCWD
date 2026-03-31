from datetime import datetime
import tkinter as tk
from tkintermapview import TkinterMapView

from database.db_incident_reports import get_incident_reports, update_incident_tubero
from database.db_locations import location_dict
from database.db_keywords import keywords_data


class MapTab:

    def __init__(self, parent, email, role):
        self.bounds = {
            "north": 8.7383383,
            "south": 8.5496192,
            "east": 123.5536909,
            "west": 123.3028289,
        }

        self.email = email
        self.role = role
        self.frame = tk.Frame(parent)

        control = tk.Frame(self.frame)
        control.pack(fill="x", padx=10, pady=5)

        # --- Filter controls ---
        tk.Label(control, text="Condition:").pack(side="left", padx=(10, 2))
        self.condition_filter = tk.StringVar(value="All")
        condition_options = ["All", "High Priority"]
        tk.OptionMenu(control, self.condition_filter, *condition_options).pack(
            side="left"
        )

        tk.Label(control, text="Status:").pack(side="left", padx=(10, 2))
        self.status_filter = tk.StringVar(value="All")
        status_options = ["All", "Pending", "Handled"]
        tk.OptionMenu(control, self.status_filter, *status_options).pack(side="left")

        unique_categories = sorted(list(set(row[2].lower() for row in keywords_data)))

        tk.Label(control, text="Category:").pack(side="left", padx=(10, 2))
        self.category_filter = tk.StringVar(value="All")

        # Build the options: "All" + the unique list
        category_options = ["All"] + unique_categories

        tk.OptionMenu(control, self.category_filter, *category_options).pack(
            side="left"
        )

        tk.Label(control, text="Show incidents:").pack(side="left")

        self.limit_var = tk.IntVar(value=15)
        tk.Entry(control, textvariable=self.limit_var, width=5).pack(
            side="left", padx=5
        )

        tk.Button(control, text="Refresh", command=self.refresh).pack(
            side="left", padx=10
        )

        # ---------- MAIN LAYOUT ----------
        content = tk.Frame(self.frame)
        content.pack(fill="both", expand=True)

        map_container = tk.Frame(content)
        map_container.pack(side="left", fill="both", expand=True)

        list_container = tk.Frame(content)
        list_container.pack(side="right", fill="y")

        # ---------- INCIDENT PANEL ----------
        tk.Label(list_container, text="Incidents", font=("Arial", 11, "bold")).pack(
            pady=5
        )

        # Container for canvas and scrollbar to sit side-by-side
        canvas_frame = tk.Frame(list_container)
        canvas_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(
            canvas_frame, width=250, highlightthickness=0
        )  # Increased width slightly
        scroll = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)

        self.incident_panel = tk.Frame(canvas)

        # Create the canvas window and capture the ID
        self.canvas_window = canvas.create_window(
            (0, 0), window=self.incident_panel, anchor="nw"
        )

        # 1. Update scrollregion when panel size changes
        self.incident_panel.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # 2. IMPORTANT: Update internal frame width when canvas resizes
        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfig(self.canvas_window, width=e.width),
        )

        canvas.configure(yscrollcommand=scroll.set)

        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # MAPS
        self.map_widget = TkinterMapView(map_container)
        self.map_widget.canvas.unbind("<MouseWheel>")
        self.map_widget.canvas.unbind("<Double-Button-1>")
        self.map_widget.canvas.bind("<B1-Motion>", self.limit_panning, add="+")
        self.map_widget.canvas.bind("<ButtonRelease-1>", self.limit_panning, add="+")

        self.map_widget.pack(fill="both", expand=True)

        center_lat = (self.bounds["north"] + self.bounds["south"]) / 2
        center_lon = (self.bounds["east"] + self.bounds["west"]) / 2
        self.map_widget.set_position(center_lat, center_lon)

        self.map_widget.set_zoom(15)
        self.map_widget.min_zoom = 15
        self.map_widget.max_zoom = 15

        map_can = self.map_widget.canvas
        map_can.delete(self.map_widget.button_zoom_in.canvas_rect)
        map_can.delete(self.map_widget.button_zoom_in.canvas_text)
        map_can.delete(self.map_widget.button_zoom_out.canvas_rect)
        map_can.delete(self.map_widget.button_zoom_out.canvas_text)

        self.map_widget.set_polygon(
            [
                (self.bounds["north"], self.bounds["west"]),
                (self.bounds["north"], self.bounds["east"]),
                (self.bounds["south"], self.bounds["east"]),
                (self.bounds["south"], self.bounds["west"]),
            ],
            outline_color="red",
            fill_color=None,
        )

        self.markers = {}
        self.refresh()

    def limit_panning(self, event=None):
        """Constrains the map view to the defined lat/lon bounds."""
        lat, lon = self.map_widget.get_position()

        new_lat = max(self.bounds["south"], min(lat, self.bounds["north"]))
        new_lon = max(self.bounds["west"], min(lon, self.bounds["east"]))

        if new_lat != lat or new_lon != lon:
            self.map_widget.set_position(new_lat, new_lon)

    def focus_incident(self, event):
        selection = self.incident_list.curselection()
        if not selection:
            return

        index = selection[0]
        incident_id = self.list_ids[index]

        marker = self.markers.get(incident_id)

        if marker:
            lat, lon = marker.position
            self.map_widget.set_position(lat, lon)
            self.map_widget.set_zoom(15)

    def refresh(self):
        if hasattr(self, "_refresh_id"):
            self.frame.after_cancel(self._refresh_id)

        # 1. Capture current filter states
        limit_val = self.limit_var.get()
        status_sel = self.status_filter.get()
        category_sel = self.category_filter.get()
        condition_sel = self.condition_filter.get()

        # 2. Fetch data from DB
        incidents = get_incident_reports(
            limit=limit_val,
            status=status_sel,
            category=category_sel,
            condition=condition_sel,
        )

        # 3. State Change Detection (Simplified for KOS)
        current_state = set((row[0], row[8], row[7]) for row in incidents)
        if hasattr(self, "last_state") and self.last_state == current_state:
            # Check every 60s if no data change to update the "ago" text
            self._refresh_id = self.frame.after(60000, self.refresh)
            return

        self.last_state = current_state

        # 4. Clear existing UI elements
        for widget in self.incident_panel.winfo_children():
            widget.destroy()

        self.map_widget.delete_all_marker()
        self.markers.clear()

        # 5. Build the UI
        for row in incidents:
            (id, post_id, cat_id, loc_id, lat, lon, ts, cond, stat, cat_name) = row

            # --- TIME CALCULATIONS ---
            now = datetime.now()
            diff = now - ts
            days, hours = diff.days, diff.seconds // 3600
            minutes = (diff.seconds % 3600) // 60

            time_ago = (
                f"{days}d {hours}h ago"
                if days > 0
                else (f"{hours}h {minutes}m ago" if hours > 0 else f"{minutes}m ago")
            )

            # --- COLOR LOGIC FOR "AGO" ---
            # Gray (< 1h) -> Orange (1h-24h) -> Red (> 24h)
            ago_color = "#7f8c8d"  # Default Gray
            is_past_due = False

            if days >= 1:
                ago_color = "#e74c3c"  # Red (Critical)
                is_past_due = stat == "Pending"
            elif hours >= 1:
                ago_color = "#e67e22"  # Orange (Warning)

            # --- UI STYLING ---
            location = location_dict.get(loc_id)
            location_text = (
                f"{location['street']}, {location['barangay']}"
                if location
                else "Unknown"
            )

            base_color = "#3498db"  # Default Blue
            if stat == "Pending":
                base_color = "#f39c12"
            if stat == "Handled":
                base_color = "#2ecc71"
            if cond == "High Priority" or is_past_due:
                base_color = "#c0392b"  # Deep Red

            # --- RENDER CARD ---
            row_frame = tk.Frame(
                self.incident_panel,
                bd=1,
                relief="solid",
                padx=10,
                pady=10,
                bg="#ffffff",
            )
            row_frame.pack(fill="x", padx=5, pady=4)

            text_frame = tk.Frame(row_frame, bg="#ffffff")
            text_frame.pack(side="left", fill="x", expand=True)

            # Category & Priority Tag
            title = f"{cat_name.upper()}" + (" [CRITICAL]" if is_past_due else "")
            tk.Label(
                text_frame,
                text=title,
                font=("Arial", 11, "bold"),
                fg=base_color,
                bg="#ffffff",
            ).pack(anchor="w")

            # Location
            tk.Label(
                text_frame, text=f"📍 {location_text}", font=("Arial", 9), bg="#ffffff"
            ).pack(anchor="w")

            # The Visible "AGO" Label (The Focus)
            tk.Label(
                text_frame,
                text=f"⏱ {time_ago.upper()}",
                font=("Verdana", 9, "bold"),
                fg=ago_color,
                bg="#ffffff",
            ).pack(anchor="w", pady=(2, 0))

            # --- MAP MARKER ---
            self.markers[id] = self.map_widget.set_marker(
                lat, lon, text=f"{cat_name}\n{time_ago}", marker_color_circle=base_color
            )

            # --- ACTION BUTTON (TUBERO ONLY) ---
            if self.role == "tubero":
                btn_frame = tk.Frame(row_frame, bg="#ffffff")
                btn_frame.pack(side="right", padx=5)

                def open_update(pid=post_id, cur_stat=stat):
                    popup = tk.Toplevel(self.frame)
                    popup.title("Update Status")
                    popup.geometry("250x120")
                    tk.Label(popup, text="Select Status:").pack(pady=10)
                    status_var = tk.StringVar(value=cur_stat)
                    tk.OptionMenu(popup, status_var, "Pending", "Handled").pack(pady=5)

                    def save():
                        update_incident_tubero(pid, status_var.get())
                        popup.destroy()
                        self.refresh()

                    tk.Button(
                        popup,
                        text="Save",
                        command=save,
                        bg="#2ecc71",
                        fg="white",
                        padx=10,
                    ).pack(pady=10)

                tk.Button(
                    btn_frame,
                    text="Update",
                    command=open_update,
                    bg="#3498db",
                    fg="white",
                    padx=12,
                    font=("Arial", 9, "bold"),
                ).pack()

            # Interaction: Click row to focus map
            row_frame.bind(
                "<Button-1>",
                lambda e, lt=lat, ln=lon: self.map_widget.set_position(lt, ln),
            )

        # 6. Reschedule
        self._refresh_id = self.frame.after(30000, self.refresh)
