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

        # 2. Fetch data from DB (Filtering happens at the SQL level now)
        incidents = get_incident_reports(
            limit=limit_val,
            status=status_sel,
            category=category_sel,
            condition=condition_sel,
        )

        # 3. State Change Detection
        # Tracks (ID, Status) to see if we actually need to redraw the UI
        current_state = set((row[0], row[3], row[8]) for row in incidents)

        if hasattr(self, "last_state") and self.last_state == current_state:
            # No data changes, just reschedule the next check
            self._refresh_id = self.frame.after(15000, self.refresh)
            return

        # Data has changed or filters were updated; proceed with UI update
        self.last_state = current_state

        # 4. Clear existing UI elements
        for widget in self.incident_panel.winfo_children():
            widget.destroy()

        self.map_widget.delete_all_marker()
        self.markers.clear()

        # 5. Build the UI rows and Map markers
        for row in incidents:
            (id, post_id, cat_id, loc_id, lat, lon, ts, cond, stat, cat_name) = row

            # Resolve Location Text
            location = location_dict.get(loc_id)
            location_text = (
                f"{location['street']}, {location['barangay']}"
                if location
                else "Unknown Location"
            )

            # Determine marker and label colors
            if stat == "Pending":
                color = "#f39c12"  # Orange
            elif stat == "Handled":
                color = "#2ecc71"  # Green
            else:
                color = "#3498db"  # Blue (Default/Under Evaluation)

            if cond == "High Priority":
                color = "#e74c3c"  # Red overrides for priority

            # --- MAP MARKER ---
            marker_label = f"{cat_name.replace('_', ' ').title()}\n📍 {location_text}"
            marker = self.map_widget.set_marker(
                lat, lon, text=marker_label, marker_color_circle=color
            )
            self.markers[id] = marker

            # --- INCIDENT CARD (UI ROW) ---
            row_frame = tk.Frame(
                self.incident_panel, bd=1, relief="solid", padx=5, pady=5
            )
            row_frame.pack(fill="x", expand=True, padx=3, pady=3)

            text_frame = tk.Frame(row_frame)
            text_frame.pack(side="left", fill="x", expand=True)

            # Category Label
            tk.Label(
                text_frame, text=cat_name.upper(), font=("Arial", 10, "bold")
            ).pack(anchor="w", padx=5)

            # Location Label
            tk.Label(
                text_frame,
                text=f"📍 {location_text}",
                font=("Arial", 8),
                wraplength=110,
            ).pack(anchor="w", padx=5)

            # Status Label
            tk.Label(text_frame, text=stat, fg=color, font=("Arial", 8, "bold")).pack(
                anchor="w", padx=5
            )

            # Click Event: Focus map on this incident
            focus_map = lambda e, lt=lat, ln=lon: self.map_widget.set_position(lt, ln)
            row_frame.bind("<Button-1>", focus_map)
            text_frame.bind("<Button-1>", focus_map)

            # --- ACTION BUTTONS ---
            if self.role == "tubero":
                btn_frame = tk.Frame(row_frame)
                btn_frame.pack(side="right", fill="y")

                def open_update(pid=post_id, cur_stat=stat):
                    popup = tk.Toplevel(self.frame)
                    popup.title("Update Status")
                    popup.geometry("250x120")

                    tk.Label(popup, text="Select Status:").pack(pady=(10, 5))
                    status_var = tk.StringVar(value=cur_stat)
                    tk.OptionMenu(popup, status_var, "Pending", "Handled").pack(
                        pady=(0, 10)
                    )

                    def save():
                        update_incident_tubero(pid, status_var.get())
                        popup.destroy()
                        self.refresh()  # Trigger immediate refresh after DB update

                    tk.Button(
                        popup, text="Save", command=save, bg="#2ecc71", fg="white"
                    ).pack()

                tk.Button(
                    btn_frame,
                    text="Update",
                    command=open_update,
                    bg="#3498db",
                    fg="white",
                    padx=8,
                ).pack()

        # 6. Reschedule the refresh
        self._refresh_id = self.frame.after(15000, self.refresh)
