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

    def focus_incident(self, event) -> None:
        if hasattr(event.widget, "curselection"):
            selection = self.incident_list.curselection()
            if not selection:
                return
            index = selection[0]
            incident_id = self.list_ids[index]
        else:
            # If called from a direct card click, incident_id is passed via lambda
            incident_id = event

        marker = self.markers.get(incident_id)

        if marker:
            lat, lon = marker.position

            # 1. Move to position
            self.map_widget.set_position(lat, lon)

            # 2. "Zoom-In" Animation sequence
            def animate_zoom(step: int) -> None:
                if step == 1:
                    self.map_widget.set_zoom(14)
                    self.frame.after(100, lambda: animate_zoom(2))
                elif step == 2:
                    self.map_widget.set_zoom(16)
                    self.frame.after(100, lambda: animate_zoom(3))
                elif step == 3:
                    self.map_widget.set_zoom(15)  # Final Zoom

            animate_zoom(1)

    def refresh(self) -> None:
        if hasattr(self, "_refresh_id"):
            self.frame.after_cancel(self._refresh_id)

        # 1. Fetch Data
        limit_val: int = self.limit_var.get()
        status_sel: str = self.status_filter.get()
        category_sel: str = self.category_filter.get()
        condition_sel: str = self.condition_filter.get()

        incidents: list = get_incident_reports(
            limit=limit_val,
            status=status_sel,
            category=category_sel,
            condition=condition_sel,
        )

        # 2. State Change Detection
        current_state: set = set((row[0], row[8], row[7]) for row in incidents)
        if hasattr(self, "last_state") and self.last_state == current_state:
            self._refresh_id = self.frame.after(60000, self.refresh)
            return
        self.last_state = current_state

        # 3. Cleanup
        for widget in self.incident_panel.winfo_children():
            widget.destroy()
        self.map_widget.delete_all_marker()
        self.markers.clear()

        # 4. Build UI Cards
        for row in incidents:
            (id, post_id, cat_id, loc_id, lat, lon, ts, cond, stat, cat_name) = row

            # --- TIME & STYLE LOGIC ---
            now: datetime = datetime.now()
            diff = now - ts
            is_past_due: bool = diff.days >= 1 and stat == "Pending"

            # Theme Colors: fg = Circle Center, bg = Badge Background
            styles: dict = {
                "Pending": {
                    "fg": "#f39c12",
                    "bg": "#FFF4E5",
                    "border": "#FFE7BA",
                    "sym": "⏳",
                },
                "Handled": {
                    "fg": "#27ae60",
                    "bg": "#F6FFED",
                    "border": "#B7EB8F",
                    "sym": "✅",
                },
                "Critical": {
                    "fg": "#e74c3c",
                    "bg": "#FFF1F0",
                    "border": "#FFA39E",
                    "sym": "🚨",
                },
            }
            theme = (
                styles["Critical"]
                if is_past_due
                else styles.get(stat, styles["Pending"])
            )

            # --- CARD CONSTRUCTION ---
            card = tk.Frame(
                self.incident_panel,
                bg="white",
                highlightthickness=1,
                highlightbackground=theme["border"],
                cursor="hand2",
            )
            card.pack(fill="x", padx=10, pady=5)

            # Left side color accent
            accent = tk.Frame(card, bg=theme["fg"], width=5)
            accent.pack(side="left", fill="y")

            # Info container (Center)
            info_frame = tk.Frame(card, bg="white", padx=10, pady=10)
            info_frame.pack(side="left", fill="both", expand=True)

            lbl_title = tk.Label(
                info_frame,
                text=cat_name.upper(),
                font=("Arial", 10, "bold"),
                bg="white",
                fg="#2c3e50",
            )
            lbl_title.pack(anchor="w")

            loc_data = location_dict.get(loc_id, {"street": "Unknown Location"})
            lbl_loc = tk.Label(
                info_frame,
                text=f"📍 {loc_data['street']}",
                font=("Arial", 9),
                bg="white",
                fg="#7f8c8d",
            )
            lbl_loc.pack(anchor="w")

            time_str = (
                f"{diff.days}d ago" if diff.days > 0 else f"{diff.seconds//3600}h ago"
            )
            badge_frame = tk.Frame(info_frame, bg=theme["bg"], padx=6, pady=2)
            badge_frame.pack(anchor="w", pady=(5, 0))
            lbl_badge = tk.Label(
                badge_frame,
                text=f"{theme['sym']} {stat.upper()} • {time_str}",
                font=("Consolas", 8, "bold"),
                fg=theme["fg"],
                bg=theme["bg"],
            )
            lbl_badge.pack()

            # --- ACTION BUTTON (Fixed & Robust) ---
            if self.role == "tubero":
                btn_container = tk.Frame(card, bg="white", width=100)
                btn_container.pack(side="right", fill="y", padx=10)
                btn_container.pack_propagate(False)

                tk.Button(
                    btn_container,
                    text="UPDATE",
                    font=("Arial", 9, "bold"),
                    bg="#3498db",
                    fg="white",
                    relief="flat",
                    activebackground="#2980b9",
                    cursor="hand2",
                    command=lambda p=post_id, s=stat: self.open_update_popup(p, s),
                ).pack(expand=True, fill="both", pady=12)

            # --- CLICK INTERACTION (Visual Flash Animation) ---
            def handle_click(e, lt=lat, ln=lon, c=card, b=theme["border"]):
                # 1. Map Interaction (Direct positioning, no zoom bounce)
                self.map_widget.set_position(lt, ln)

                # 2. Visual "Flash" Animation on the UI Card
                # Briefly change background and border to blue highlight
                c.config(
                    highlightbackground="#3498db", highlightthickness=2, bg="#ebf5fb"
                )
                info_frame.config(bg="#ebf5fb")
                lbl_title.config(bg="#ebf5fb")
                lbl_loc.config(bg="#ebf5fb")

                def reset_style():
                    c.config(highlightbackground=b, highlightthickness=1, bg="white")
                    info_frame.config(bg="white")
                    lbl_title.config(bg="white")
                    lbl_loc.config(bg="white")

                self.frame.after(250, reset_style)

            # Bind click to every element to prevent "blocked" clicks
            for w in [
                card,
                info_frame,
                lbl_title,
                lbl_loc,
                badge_frame,
                lbl_badge,
                accent,
            ]:
                w.bind("<Button-1>", handle_click)

            # --- MAP MARKER (Blackish Outside) ---
            self.markers[id] = self.map_widget.set_marker(
                lat,
                lon,
                text=f"{theme['sym']} {cat_name}",
                marker_color_circle=theme["fg"],
                marker_color_outside="#2c3e50",  # Modern blackish-blue ring
                text_color="#2c3e50",
            )

        self._refresh_id = self.frame.after(30000, self.refresh)

    def open_update_popup(self, post_id: int, current_stat: str) -> None:
        """Full Modal for Updating Incident Status"""
        popup = tk.Toplevel(self.frame)
        popup.title("Update Status")
        popup.geometry("320x200")
        popup.configure(bg="white")
        popup.grab_set()

        # Center logic
        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - 160
        y = (popup.winfo_screenheight() // 2) - 100
        popup.geometry(f"+{int(x)}+{int(y)}")

        tk.Label(
            popup,
            text="Update Progress",
            font=("Arial", 11, "bold"),
            bg="white",
            pady=15,
        ).pack()

        status_var = tk.StringVar(value=current_stat)
        menu = tk.OptionMenu(popup, status_var, "Pending", "Handled")
        menu.config(width=15, font=("Arial", 10))
        menu.pack(pady=5)

        def save_and_refresh():
            update_incident_tubero(post_id, status_var.get())
            popup.destroy()
            self.refresh()

        tk.Button(
            popup,
            text="SAVE CHANGES",
            bg="#2ecc71",
            fg="white",
            font=("Arial", 10, "bold"),
            width=18,
            pady=10,
            relief="flat",
            command=save_and_refresh,
        ).pack(pady=20)
