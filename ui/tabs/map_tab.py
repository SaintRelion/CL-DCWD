from datetime import datetime
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkintermapview import TkinterMapView

from utils.incident_pdf_report import export_incidents_pdf
from database.db_incident_reports import get_incident_reports, update_incident_status
from database.db_locations import location_dict
from database.db_keywords import keyword_dict


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
        self.reports = []  # Storage for filtering

        # 1. TOP CONTROL BAR
        control = tk.Frame(self.frame)
        control.pack(fill="x", padx=10, pady=5)

        tk.Label(control, text="Status:").pack(side="left", padx=(10, 2))
        self.status_filter = tk.StringVar(value="All")
        status_options = ["All", "Active", "Handled", "Invalidate"]
        tk.OptionMenu(control, self.status_filter, *status_options).pack(side="left")

        tk.Label(control, text="Category:").pack(side="left", padx=(10, 2))
        self.category_filter = tk.StringVar(value="All")
        category_options = ["All"] + sorted(
            [cat.title() for cat in keyword_dict.keys()]
        )
        tk.OptionMenu(control, self.category_filter, *category_options).pack(
            side="left"
        )

        self.status_filter.trace_add("write", lambda *args: self.refresh())
        self.category_filter.trace_add("write", lambda *args: self.refresh())

        tk.Label(control, text="Show incidents:").pack(side="left", padx=(10, 2))
        self.limit_var = tk.IntVar(value=15)
        tk.Entry(control, textvariable=self.limit_var, width=5).pack(
            side="left", padx=5
        )
        tk.Button(control, text="Refresh", command=self.refresh).pack(
            side="left", padx=10
        )

        tk.Button(
            control,
            text="⬇ Export Report",
            command=self.generate_report,
            bg="#2C5F8A",
            fg="white",
            relief="flat",
            padx=8,
        ).pack(side="left", padx=6)

        # 2. MAIN CONTENT AREA
        content = tk.Frame(self.frame)
        content.pack(fill="both", expand=True)

        # MAP (Left)
        map_container = tk.Frame(content)
        map_container.pack(side="left", fill="both", expand=True)

        # SIDEBAR (Right) - We define self.sidebar here to fix the AttributeError
        self.sidebar = tk.Frame(content, width=300, bg="white", bd=1, relief="ridge")
        self.sidebar.pack(side="right", fill="y")
        self.sidebar.pack_propagate(False)

        canvas_frame = tk.Frame(self.sidebar, bg="white")
        canvas_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(canvas_frame, highlightthickness=0, bg="white")
        scroll = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        self.incident_panel = tk.Frame(canvas, bg="white")
        self.incident_panel.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        self.canvas_window = canvas.create_window(
            (0, 0), window=self.incident_panel, anchor="nw"
        )

        # 3. SIDEBAR SEARCH
        search_frame = tk.Frame(self.sidebar, bg="white")
        search_frame.pack(fill="x", padx=5, pady=10)

        tk.Label(search_frame, text="🔍", bg="white").pack(side="left", padx=2)
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.render_sidebar())

        search_entry = tk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=("Arial", 11),
            bd=1,
            relief="solid",
        )
        search_entry.insert(0, "Search ID...")
        search_entry.bind(
            "<FocusIn>",
            lambda e: (
                self.search_var.set("")
                if self.search_var.get() == "Search ID..."
                else None
            ),
        )
        search_entry.pack(side="left", fill="x", expand=True, padx=5, ipady=3)

        # 4. SCROLLABLE INCIDENT LIST
        tk.Label(
            self.sidebar, text="Incident List", font=("Arial", 10, "bold"), bg="white"
        ).pack(pady=2)

        self.incident_panel.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfig(self.canvas_window, width=e.width),
        )

        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # 5. MAP INITIALIZATION
        self.map_widget = TkinterMapView(map_container)
        # Prevent default behaviors that might interfere with custom panning
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

        # Clean up default buttons
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
        lat, lon = self.map_widget.get_position()
        new_lat = max(self.bounds["south"], min(lat, self.bounds["north"]))
        new_lon = max(self.bounds["west"], min(lon, self.bounds["east"]))

        if new_lat != lat or new_lon != lon:
            self.map_widget.set_position(new_lat, new_lon)

    def _create_incident_card(self, report: tuple) -> None:
        """Shared method to render a single incident card in the sidebar."""
        # Unpack SQL row (7 columns)
        inc_id, ts, cat_name, loc_id, street_name, plumber, stat, remarks = report

        # Resolve location data
        loc_data = location_dict.get(
            loc_id, {"barangay": "Unknown", "latitude": 0.0, "longitude": 0.0}
        )
        brgy, lat, lon = (
            loc_data["barangay"],
            loc_data["latitude"],
            loc_data["longitude"],
        )

        # Theme Logic
        now = datetime.now()
        diff = now - ts
        is_past_due = diff.days >= 1 and stat == "Active"

        styles = {
            "Active": {
                "fg": "#d35400",
                "bg": "#fff5e6",
                "border": "#f39c12",
                "sym": "⏳",
            },
            "Closed": {
                "fg": "#27ae60",
                "bg": "#f0fff4",
                "border": "#2ecc71",
                "sym": "✅",
            },
            "Invalidate": {
                "fg": "#7f8c8d",
                "bg": "#f8f9f9",
                "border": "#bdc3c7",
                "sym": "❌",
            },
            "Critical": {
                "fg": "#c0392b",
                "bg": "#fff5f5",
                "border": "#e74c3c",
                "sym": "🚨",
            },
        }
        theme = (
            styles["Critical"] if is_past_due else styles.get(stat, styles["Active"])
        )

        # Main Card Frame
        card = tk.Frame(
            self.incident_panel,
            bg=theme["bg"],
            highlightthickness=1,
            highlightbackground=theme["border"],
            cursor="hand2",
        )
        card.pack(fill="x", padx=10, pady=5)

        accent = tk.Frame(card, bg=theme["fg"], width=5)
        accent.pack(side="left", fill="y")

        info_frame = tk.Frame(card, bg=theme["bg"], padx=10, pady=10)
        info_frame.pack(side="left", fill="both", expand=True)

        # Header: ID and Category
        header_row = tk.Frame(info_frame, bg=theme["bg"])
        header_row.pack(fill="x")

        tk.Label(
            header_row,
            text=f" #{inc_id} ",
            font=("Arial", 10, "bold"),
            bg="#2c3e50",
            fg="white",
        ).pack(side="left", padx=(0, 10))

        tk.Label(
            header_row,
            text=cat_name.upper(),
            font=("Arial", 12, "bold"),
            bg=theme["bg"],
            fg="#2c3e50",
        ).pack(side="left")

        # Location
        display_street = f"{street_name}, " if street_name else ""
        tk.Label(
            info_frame,
            text=f"📍 {display_street}Brgy. {brgy}",
            font=("Arial", 10),
            bg=theme["bg"],
            fg="#34495e",
        ).pack(anchor="w")

        # Badge Frame
        time_str = (
            f"{diff.days}d ago" if diff.days > 0 else f"{diff.seconds//3600}h ago"
        )
        badge_frame = tk.Frame(
            info_frame, bg="white", padx=6, pady=2, bd=1, relief="solid"
        )
        badge_frame.pack(anchor="w", pady=(5, 0))

        tk.Label(
            badge_frame,
            text=f"{theme['sym']} {(stat if stat != 'Closed' else 'Handled').upper()} • {time_str}",
            font=("Consolas", 9, "bold"),
            fg=theme["fg"],
            bg="white",
        ).pack()

        # Reconstruct full data for the map zoom
        full_data = (inc_id, ts, cat_name, brgy, street_name, plumber, stat, lat, lon)

        # Unified Click Handler
        def handle_click(e):
            if lat != 0.0:
                self.map_widget.set_position(lat, lon)
                self.map_widget.set_zoom(18)
            card.config(bg="#d4e6f1")
            info_frame.config(bg="#d4e6f1")
            self.frame.after(
                200,
                lambda: [
                    card.config(bg=theme["bg"]),
                    info_frame.config(bg=theme["bg"]),
                ],
            )

        # Bindings
        for w in [card, info_frame, badge_frame, accent]:
            w.bind("<Button-1>", handle_click)
            for child in w.winfo_children():
                child.bind("<Button-1>", handle_click)

        if lat != 0.0 and lon != 0.0:
            self.markers[inc_id] = self.map_widget.set_marker(
                lat,
                lon,
                text=f"#{inc_id} {cat_name}",
                marker_color_circle=theme["fg"],
            )

    def refresh(self) -> None:
        if hasattr(self, "_refresh_id"):
            self.frame.after_cancel(self._refresh_id)

        limit_val: int = self.limit_var.get()
        status_sel: str = self.status_filter.get()
        category_sel: str = self.category_filter.get()

        db_status = "Closed" if status_sel == "Handled" else status_sel

        # Ensure normalized category for DB
        db_category = category_sel
        if category_sel != "All":
            db_category = category_sel.lower().replace(" ", "_")

        incidents: list = get_incident_reports(
            limit=limit_val,
            status=db_status,
            category=db_category,
            show_test_data=False,
        )

        self.reports = incidents

        # row[6] is status in the 7-column return
        current_state: set = set((row[0], row[6]) for row in incidents)
        if hasattr(self, "last_state") and self.last_state == current_state:
            self._refresh_id = self.frame.after(60000, self.refresh)
            return
        self.last_state = current_state

        for widget in self.incident_panel.winfo_children():
            widget.destroy()

        self.map_widget.delete_all_marker()
        self.markers.clear()

        for row in incidents:
            self._create_incident_card(row)

        self._refresh_id = self.frame.after(30000, self.refresh)

    def render_sidebar(self) -> None:
        for widget in self.incident_panel.winfo_children():
            widget.destroy()

        query = self.search_var.get().lower().strip()

        for report in self.reports:
            inc_id, _, cat_name, loc_id, _, _, _ = report
            brgy = location_dict.get(loc_id, {}).get("barangay", "").lower()

            if (
                query
                and query not in str(inc_id)
                and query not in cat_name.lower()
                and query not in brgy
            ):
                continue

            self._create_incident_card(report)

    def focus_on_report(self, report: tuple) -> None:
        inc_id, ts, cat, brgy, street, plumber, status, lat, lon = report

        if lat and lon:
            self.map_widget.set_position(lat, lon)
            self.map_widget.set_zoom(18)

            # # 2. Open the edit popup for this specific incident
            # self.show_report_details(report)

    def open_update_popup(self, incident_id: int, current_stat: str) -> None:
        popup: tk.Toplevel = tk.Toplevel(self.frame)
        popup.title(f"Update Case #{incident_id}")
        popup.geometry("340x280")
        popup.configure(bg="white")
        popup.grab_set()

        popup.update_idletasks()
        x = (popup.winfo_screenwidth() // 2) - 170
        y = (popup.winfo_screenheight() // 2) - 140
        popup.geometry(f"+{int(x)}+{int(y)}")

        tk.Label(
            popup,
            text="Case Resolution",
            font=("Arial", 12, "bold"),
            bg="white",
            pady=10,
        ).pack()

        initial_ui_stat = "Handled" if current_stat == "Closed" else current_stat

        status_var = tk.StringVar(value=initial_ui_stat)
        menu = tk.OptionMenu(popup, status_var, "Active", "Handled", "Invalidate")
        menu.config(width=18, font=("Arial", 11))
        menu.pack(pady=5)

        remarks_frame = tk.Frame(popup, bg="white")
        tk.Label(
            remarks_frame,
            text="Remarks / Resolution Notes:",
            font=("Arial", 10),
            bg="white",
        ).pack(anchor="w", pady=(10, 2))
        remarks_var = tk.StringVar()
        tk.Entry(
            remarks_frame,
            textvariable=remarks_var,
            font=("Arial", 11),
            width=32,
            relief="solid",
            bd=1,
        ).pack(ipady=4)

        def toggle_remarks(*args):
            if status_var.get() == "Handled":
                remarks_frame.pack(fill="x", padx=25, pady=5)
            else:
                remarks_frame.pack_forget()
                remarks_var.set("")

        status_var.trace_add("write", toggle_remarks)
        toggle_remarks()

        def save_and_refresh():
            new_ui_status: str = (
                status_var.get()
            )  # "Active", "Handled", or "Invalidate"

            # Map UI "Handled" to DB "Closed"
            new_db_status: str = (
                "Closed" if new_ui_status == "Handled" else new_ui_status
            )
            remarks_text: str = remarks_var.get()

            if update_incident_status(incident_id, new_db_status, remarks_text):
                popup.destroy()
                self.refresh()

        tk.Button(
            popup,
            text="SAVE CHANGES",
            bg="#2ecc71",
            fg="white",
            font=("Arial", 11, "bold"),
            width=20,
            pady=8,
            relief="flat",
            command=save_and_refresh,
        ).pack(pady=15)

    def generate_report(self) -> None:
        if not hasattr(self, "reports") or not self.reports:
            messagebox.showwarning(
                "No Data", "No incidents loaded. Press Refresh first."
            )
            return

        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")],
            initialfile=f"incident_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
            title="Save Incident Report",
        )
        if not output_path:
            return  # user cancelled

        try:
            export_incidents_pdf(
                incidents=self.reports,
                output_path=output_path,
                title="Water Incident Report",
            )
            if messagebox.askyesno("Report Saved", f"Report saved.\n\nOpen file now?"):
                os.startfile(
                    output_path
                )  # Windows — use subprocess.run(["open", ...]) on Mac
        except Exception as e:
            messagebox.showerror("Export Failed", str(e))
