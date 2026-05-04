import tkinter as tk
from tkinter import ttk
from utils.incident_email import send_incident_email
from database.db_posts import get_posts, update_post_operator


class NotificationsTab:

    def __init__(self, parent, nlp, lv, email, role):
        self.nlp = nlp
        self.lv = lv
        self.email = email
        self.role = role

        self.frame = tk.Frame(parent)

        # --- Control panel ---
        control = tk.Frame(self.frame)
        control.pack(fill="x", padx=10, pady=5)

        tk.Label(control, text="Show posts:").pack(side="left")

        self.limit_var = tk.IntVar(value=10)
        tk.Entry(control, textvariable=self.limit_var, width=5).pack(
            side="left", padx=5
        )
        tk.Button(control, text="Refresh", command=self.refresh).pack(
            side="left", padx=10
        )

        # Dropdown for filtering operator status
        tk.Label(control, text="Filter Status:").pack(side="left", padx=(10, 2))

        self.filter_var = tk.StringVar(value="All")  # default: show all
        filter_options = [
            "All",
            "False Report",
            "Non-Incident",
            "Actual Incident",
            "Under Evaluation",
        ]
        tk.OptionMenu(control, self.filter_var, *filter_options).pack(side="left")
        self.filter_var.trace_add("write", lambda *args: self.refresh())

        # --- Scrollable container ---
        canvas = tk.Canvas(self.frame, bg="#f9f9f9", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        # Create the inner frame
        self.container = tk.Frame(canvas, bg="#f9f9f9")
        container_window = canvas.create_window(
            (0, 0), window=self.container, anchor="nw"
        )

        # Update scroll region
        self.container.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Make inner frame width track canvas width
        def on_canvas_configure(event):
            canvas.itemconfig(container_window, width=event.width)

        canvas.bind("<Configure>", on_canvas_configure)

        # Header
        tk.Label(
            self.container,
            text="Incoming Posts",
            font=("Arial", 18, "bold"),
            bg="#f9f9f9",
        ).pack(anchor="w", pady=(0, 10))

        self.refresh()

    def refresh(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        current_filter = self.filter_var.get()
        limit_val = self.limit_var.get()

        # 3. Fetch filtered posts
        posts = get_posts(status_filter=current_filter, limit=limit_val)

        for row in posts:
            post_id, post_text, status, loc_id, lat, lon, intent, score = row

            score = float(score)

            location = next(
                (r for r in self.lv.location_rows if r["id"] == loc_id), None
            )
            if location:
                location_text = f"📍 {location['street']}, {location['barangay']}"
            else:
                location_text = "📍 Location: Not yet identified"

            # Background color logic based on Status or Confidence
            if status == "Actual Incident":
                bg_color = "#d4edda"  # Success Green
            elif status == "False Report" or status == "Non-Incident":
                bg_color = "#f8d7da"  # Danger Red
            elif score < 0.5:
                bg_color = "#fff3cd"  # Warning Yellow
            else:
                bg_color = "#ffffff"  # Default White

            # --- Post Card Frame ---
            frame = tk.Frame(
                self.container, bd=1, relief="solid", padx=10, pady=10, bg=bg_color
            )
            frame.pack(fill="x", pady=5, padx=10)

            # Post Content
            tk.Label(
                frame,
                text=post_text,
                wraplength=600,
                justify="left",
                bg=bg_color,
                font=("Arial", 14),
            ).pack(anchor="w")

            # Intent & Confidence
            meta_info = (
                f"Detected Intent: {intent.upper()} | AI Confidence: {score:.2%}"
            )
            tk.Label(
                frame,
                text=meta_info,
                bg=bg_color,
                font=("Arial", 11, "italic"),
                fg="#555",
            ).pack(anchor="w", pady=(2, 0))

            # --- ADDED: Location Display ---
            tk.Label(
                frame,
                text=location_text,
                bg=bg_color,
                font=("Arial", 11, "bold"),
                fg="#2c3e50",
            ).pack(anchor="w", pady=(2, 5))

            # Footer / Status & Action
            footer = tk.Frame(frame, bg=bg_color)
            footer.pack(fill="x", pady=(5, 0))

            tk.Label(
                footer,
                text=f"Operator Status: {status}",
                bg=bg_color,
                font=("Arial", 11, "bold"),
            ).pack(side="left")

            # Action Button
            tk.Button(
                footer,
                text="Review & Action",
                command=lambda p=post_id, t=post_text, l=loc_id, i=intent: self.open_status_popup(
                    p, t, l, i
                ),
                font=("Arial", 11),
            ).pack(side="right")

    def open_status_popup(
        self, post_id, post_text, location_id=None, intent_word="Unknown"
    ):
        popup = tk.Toplevel(self.frame)
        popup.title("Review Post")
        popup.geometry("380x250")  # Dynamic resizing handled below
        popup.padx = 15

        # --- Post Context ---
        tk.Label(popup, text="Original Post:", font=("Arial", 11, "bold")).pack(
            anchor="w", padx=15, pady=(10, 0)
        )
        tk.Label(
            popup,
            text=post_text[:120] + "...",
            wraplength=340,
            justify="left",
            fg="#444",
        ).pack(anchor="w", padx=15)

        # --- Decision Dropdown ---
        tk.Label(popup, text="Set Status:", font=("Arial", 11, "bold")).pack(
            pady=(10, 0)
        )
        operator_var = tk.StringVar(value="Under Evaluation")
        options = [
            "Under Evaluation",
            "Actual Incident",
            "Non-Incident",
            "False Report",
        ]
        tk.OptionMenu(popup, operator_var, *options).pack(fill="x", padx=30)

        # --- Conditional Inputs (Only for Actual Incident) ---
        extra_frame = tk.Frame(popup)

        # Priority/Condition
        tk.Label(extra_frame, text="Priority Level:").pack(anchor="w")
        condition_var = tk.StringVar(value="None")
        tk.OptionMenu(extra_frame, condition_var, "None", "High Priority").pack(
            fill="x", pady=(0, 10)
        )

        # Location Mapping (Street, Barangay -> ID)
        tk.Label(extra_frame, text="Verify/Assign Location:").pack(anchor="w")

        # Create display mapping for the dropdown
        loc_map = {
            f"{r['street']}, {r['barangay']}": r["id"] for r in self.lv.location_rows
        }
        loc_options = sorted(list(loc_map.keys()))

        # Determine default selection
        default_loc = "Search/Select Location..."
        if location_id:
            for name, lid in loc_map.items():
                if lid == location_id:
                    default_loc = name
                    break

        location_name_var = tk.StringVar(value=default_loc)
        tk.OptionMenu(extra_frame, location_name_var, *loc_options).pack(fill="x")

        # --- Dynamic UI Toggle ---
        def toggle_inputs(*args):
            if operator_var.get() == "Actual Incident":
                extra_frame.pack(fill="x", padx=30, pady=10)
                popup.geometry("380x480")
            else:
                extra_frame.pack_forget()
                popup.geometry("380x250")

        operator_var.trace_add("write", toggle_inputs)
        toggle_inputs()  # Initialize

        # --- Save Function ---
        def save_changes():
            selected_display_text = location_name_var.get()
            selected_id = loc_map.get(selected_display_text)

            selected_loc_row = next(
                (r for r in self.lv.location_rows if r["id"] == selected_id), None
            )

            # Update DB
            update_post_operator(
                post_id,
                post_text,
                status=operator_var.get(),
                condition=condition_var.get(),
                location_row=selected_loc_row,  # Passing the full dict here
                intent_word=intent_word,
            )

            if operator_var.get() == "Actual Incident":
                incident_details = {
                    "category": intent_word,  # Passed from the main loop
                    "location": selected_display_text,
                    "priority": condition_var.get(),
                    "latitude": (
                        selected_loc_row["latitude"] if selected_loc_row else None
                    ),
                    "longitude": (
                        selected_loc_row["longitude"] if selected_loc_row else None
                    ),
                    "raw_text": post_text,
                }
                send_incident_email(incident_details)

            popup.destroy()
            self.refresh()

        tk.Button(
            popup,
            text="Confirm Decision",
            bg="#3498db",
            fg="white",
            font=("Arial", 12, "bold"),
            command=save_changes,
        ).pack(pady=20)
