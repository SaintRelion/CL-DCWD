import os
import tempfile
import webbrowser
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch

import tkinter as tk
from tkinter import ttk
from typing import Any, Dict, List, Optional
import webbrowser
from database.db_base import db_cursor
from database.db_users import get_all_tubero_names
from database.db_posts import get_posts, update_post_operator
from database.db_incident_reports import open_incident_case
from database.db_keywords import keyword_dict


class NotificationsTab:
    def __init__(self, parent: tk.Widget, lv: Any, email: str, role: str) -> None:
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

        tk.Label(control, text="Filter Status:").pack(side="left", padx=(10, 2))

        self.filter_var = tk.StringVar(value="All")
        filter_options: List[str] = [
            "All",
            "false-report",
            "non-incident",
            "actual incident",
            "under evaluation",
        ]
        tk.OptionMenu(control, self.filter_var, *filter_options).pack(side="left")
        self.filter_var.trace_add("write", lambda *args: self.refresh())

        # --- Scrollable container ---
        canvas = tk.Canvas(self.frame, bg="#f9f9f9", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        self.container = tk.Frame(canvas, bg="#f9f9f9")
        container_window = canvas.create_window(
            (0, 0), window=self.container, anchor="nw"
        )

        self.container.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.bind(
            "<Configure>", lambda e: canvas.itemconfig(container_window, width=e.width)
        )

        tk.Label(
            self.container,
            text="Incoming Posts",
            font=("Arial", 18, "bold"),
            bg="#f9f9f9",
        ).pack(anchor="w", pady=(0, 10))

        self.refresh()

    def refresh(self) -> None:
        for widget in self.container.winfo_children():
            widget.destroy()

        current_filter: str = self.filter_var.get()
        limit_val: int = self.limit_var.get()

        posts = get_posts(status_filter=current_filter, limit=limit_val)

        for row in posts:
            (
                post_id,
                post_text,
                username,
                profile_link,
                date_scraped,
                status,
                loc_id,
                lat,
                lon,
                intent,
                scraper_init,
                incident_id,
            ) = row

            location = next(
                (r for r in self.lv.location_rows if r["id"] == loc_id), None
            )
            if location:
                location_text: str = f"📍 Brgy. {location['barangay']}"
            else:
                location_text: str = "📍 Location: Not yet identified"

            is_done = False
            if status == "actual incident":
                bg_color: str = "#f7d6d8"
            elif status in ["handled", "completed", "closed"]:
                bg_color: str = "#d3f5db"
                is_done = True
            elif status in ["false-report", "non-incident"]:
                bg_color: str = "#e9e9e9"
            else:
                bg_color: str = "#ffffff"

            frame = tk.Frame(
                self.container, bd=1, relief="solid", padx=10, pady=10, bg=bg_color
            )
            frame.pack(fill="x", pady=5, padx=10)

            if incident_id:
                tk.Label(
                    frame,
                    text=f"TICKET #{incident_id}",
                    font=("Arial", 9, "bold"),
                    bg="#2c3e50",
                    fg="white",
                    padx=5,
                ).pack(anchor="e")

            tk.Label(
                frame,
                text=post_text,
                wraplength=600,
                justify="left",
                bg=bg_color,
                font=("Arial", 14),
            ).pack(anchor="w")

            meta_frame = tk.Frame(frame, bg=bg_color)
            meta_frame.pack(anchor="w", pady=(2, 0))

            tk.Label(
                meta_frame,
                text=f"Intent: {(intent or 'Unknown').upper()} | User: ",
                bg=bg_color,
                font=("Arial", 11, "italic"),
                fg="#555",
            ).pack(side="left")

            link_lbl = tk.Label(
                meta_frame,
                text=username,
                bg=bg_color,
                font=("Arial", 11, "italic", "underline"),
                fg="blue",
                cursor="hand2",
            )
            link_lbl.pack(side="left")
            link_lbl.bind(
                "<Button-1>",
                lambda e, url=profile_link: webbrowser.open(url) if url else None,
            )

            tk.Label(
                frame,
                text=location_text,
                bg=bg_color,
                font=("Arial", 11, "bold"),
                fg="#2c3e50",
            ).pack(anchor="w", pady=(2, 5))

            # --- FOOTER BUTTONS ---
            footer = tk.Frame(frame, bg=bg_color)
            footer.pack(fill="x", pady=(5, 0))

            tk.Label(
                footer,
                text=f"Status: {status.title()}",
                bg=bg_color,
                font=("Arial", 11, "bold"),
            ).pack(side="left")

            # Condition: If it's already an incident, show PRINT. Otherwise, show OPEN CASE.
            if not is_done:
                # FB Flag Button
                flag_btn = tk.Button(
                    footer,
                    text="🚩",
                    bg="#e2e3e5",
                    fg="#e74c3c",
                    font=("Arial", 10, "bold"),
                    relief="raised",
                    padx=10,  # Added X Padding
                )
                flag_btn.pack(side="left", padx=(0, 15))  # Increased side margin
                flag_btn.bind(
                    "<Button-1>", lambda e, pid=post_id: self.show_flag_menu(e, pid)
                )

                if status == "actual incident":
                    tk.Button(
                        footer,
                        text="🖨️ PRINT TICKET",
                        bg="#2ecc71",
                        fg="white",
                        font=("Arial", 10, "bold"),
                        padx=15,  # Added X Padding
                        command=lambda p=post_id: self.print_incident_ticket(p),
                    ).pack(side="right")
                else:
                    tk.Button(
                        footer,
                        text="📋 OPEN CASE",
                        bg="#3498db",
                        fg="white",
                        font=("Arial", 10, "bold"),
                        padx=15,  # Added X Padding
                        command=lambda p=post_id, t=post_text, l=loc_id, i=intent, u=username: self.open_receipt_popup(
                            p, t, l, i, u
                        ),
                    ).pack(side="right")
            else:
                # Show a "Case Resolved" text instead of buttons
                tk.Label(
                    footer,
                    text="✔️ CASE RESOLVED",
                    bg=bg_color,
                    fg="#27ae60",
                    font=("Arial", 10, "bold italic"),
                ).pack(side="right", padx=15)

    def show_flag_menu(self, event: Any, post_id: int) -> None:
        menu = tk.Menu(self.frame, tearoff=0, font=("Arial", 10))
        menu.add_command(
            label="Flag as False Report",
            command=lambda: self.execute_flag(post_id, "false-report"),
        )
        menu.add_command(
            label="Flag as Non-Incident",
            command=lambda: self.execute_flag(post_id, "non-incident"),
        )
        menu.tk_popup(event.x_root, event.y_root)

    def execute_flag(self, post_id: int, db_status: str) -> None:
        update_post_operator(post_id=post_id, status=db_status)
        self.refresh()

    def print_incident_ticket(self, post_id: int) -> None:
        """Generates a PDF work order and opens it for manual printing."""

        # 1. Fetch data from DB
        db_cursor.execute(
            """
            SELECT ir.id, ir.timestamp, k.category, l.barangay, ir.street_name, ir.plumber_name, p.raw_post_text
            FROM incident_reports ir
            LEFT JOIN keywords k ON ir.keyword_category_id = k.id
            LEFT JOIN locations l ON ir.location_id = l.id
            LEFT JOIN posts p ON ir.post_id = p.id
            WHERE ir.post_id = %s
        """,
            (post_id,),
        )

        row = db_cursor.fetchone()
        if not row:
            return

        incident_db_id, timestamp, category, barangay, street, plumber, post_text = row

        # 2. Setup PDF Temporary File
        temp_dir = tempfile.gettempdir()
        pdf_path = os.path.join(temp_dir, f"WorkOrder_{incident_db_id}.pdf")

        c = canvas.Canvas(pdf_path, pagesize=LETTER)
        width, height = LETTER

        # --- DRAWING THE TICKET ---
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(
            width / 2, height - 1 * inch, "OFFICIAL DISPATCH WORK ORDER"
        )

        c.setFont("Helvetica", 10)
        readable_date: str = (
            timestamp.strftime("%B %d, %Y - %I:%M %p") if timestamp else "N/A"
        )
        c.drawCentredString(
            width / 2, height - 1.2 * inch, f"Generated on: {readable_date}"
        )

        # Section: Incident Details
        c.line(0.5 * inch, height - 1.5 * inch, 7.5 * inch, height - 1.5 * inch)

        y = height - 1.8 * inch
        c.setFont("Helvetica-Bold", 12)
        c.drawString(0.7 * inch, y, f"TICKET ID: #{incident_db_id}")
        c.drawString(4.0 * inch, y, f"CATEGORY: {(category or 'N/A').upper()}")

        y -= 0.3 * inch
        c.setFont("Helvetica", 11)
        c.drawString(0.7 * inch, y, f"LOCATION: Brgy. {barangay or 'N/A'}")
        if street:
            c.drawString(4.0 * inch, y, f"STREET: {street}")

        y -= 0.4 * inch
        c.setFont("Helvetica-Bold", 11)
        c.drawString(0.7 * inch, y, f"ASSIGNED PLUMBER: {plumber or 'Unassigned'}")

        # Section: Raw Report (Context)
        y -= 0.6 * inch
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(0.7 * inch, y, "Original Social Media Report:")
        y -= 0.2 * inch

        # Simple text wrap for the raw post
        text_obj = c.beginText(0.7 * inch, y)
        text_obj.setFont("Helvetica-Oblique", 9)
        # Wrap text to ~70 chars
        wrapped_text = [post_text[i : i + 80] for i in range(0, len(post_text), 80)]
        for line in wrapped_text:
            text_obj.textLine(line)
        c.drawText(text_obj)

        # --- PEN/HANDWRITTEN REMARKS SECTION ---
        # We move the cursor down further to create the "Vertical Space"
        y_remarks = y - (len(wrapped_text) * 0.15 * inch) - 0.5 * inch

        c.setFont("Helvetica-Bold", 12)
        c.drawString(0.7 * inch, y_remarks, "PLUMBER REMARKS (Handwritten Report):")

        # Draw a large box for the pen report
        box_height = 3.0 * inch
        c.setDash(3, 3)  # Dashed lines look better for handwriting areas
        c.rect(0.7 * inch, y_remarks - box_height - 0.1 * inch, 6.8 * inch, box_height)

        # Footer
        c.setDash(1, 0)  # Back to solid
        c.setFont("Helvetica", 8)
        c.drawCentredString(
            width / 2,
            0.5 * inch,
            "Please return this form to the office once the maintenance is completed.",
        )

        c.showPage()
        c.save()

        # 3. Open the PDF for the user
        webbrowser.open(f"file://{pdf_path}")

    def open_receipt_popup(
        self,
        post_id: int,
        post_text: str,
        location_id: Optional[int] = None,
        intent_word: str = "Unknown",
        username: str = "Unknown",
    ) -> None:
        intent_word = intent_word or "Unknown"
        username = username or "Unknown"

        popup = tk.Toplevel(self.frame)
        popup.title("Dispatch Ticket")
        popup.geometry("480x450")  # Widened slightly to accommodate larger fields
        popup.padx = 15

        ticket_frame = tk.Frame(
            popup, bg="white", bd=2, relief="solid", padx=15, pady=15
        )
        ticket_frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            ticket_frame,
            text="=== WORK ORDER TICKET ===",
            font=("Courier", 12, "bold"),
            bg="white",
        ).pack(pady=(0, 10))

        tk.Label(
            ticket_frame,
            text=f"Name:    {username}",
            font=("Courier", 10),
            bg="white",
            anchor="w",
        ).pack(fill="x", pady=(0, 10))

        # --- PROBLEM DROPDOWN ---
        prob_frame = tk.Frame(ticket_frame, bg="white")
        prob_frame.pack(fill="x", pady=2)
        tk.Label(
            prob_frame,
            text="Problem:",
            font=("Courier", 10),
            bg="white",
            width=10,
            anchor="w",
        ).pack(side="left")

        category_options: List[str] = list(keyword_dict.keys())
        if not category_options:
            category_options = [intent_word]

        # Default to the NLP predicted intent, else fallback to the first category
        default_intent: str = (
            intent_word.lower()
            if intent_word.lower() in category_options
            else category_options[0]
        )
        problem_var = tk.StringVar(value=default_intent)
        tk.OptionMenu(prob_frame, problem_var, *category_options).pack(
            side="left", fill="x", expand=True
        )

        # --- LOCATION DROPDOWN ---
        loc_frame = tk.Frame(ticket_frame, bg="white")
        loc_frame.pack(fill="x", pady=2)
        tk.Label(
            loc_frame,
            text="Location:",
            font=("Courier", 10),
            bg="white",
            width=10,
            anchor="w",
        ).pack(side="left")

        loc_map: Dict[str, int] = {
            r["barangay"]: r["id"] for r in self.lv.location_rows if "barangay" in r
        }
        loc_options: List[str] = sorted(list(loc_map.keys()))
        if not loc_options:
            loc_options = ["None"]

        default_loc: str = loc_options[0]
        if location_id:
            for name, lid in loc_map.items():
                if lid == location_id:
                    default_loc = name
                    break

        location_name_var = tk.StringVar(value=default_loc)
        tk.OptionMenu(loc_frame, location_name_var, *loc_options).pack(
            side="left", fill="x", expand=True
        )

        # --- STREET TEXTFIELD (OPTIONAL) ---
        street_frame = tk.Frame(ticket_frame, bg="white")
        street_frame.pack(fill="x", pady=2)
        tk.Label(
            street_frame,
            text="Street(Opt):",  # Indicates it is optional
            font=("Courier", 10),
            bg="white",
            width=12,
            anchor="w",
        ).pack(side="left")

        street_var = tk.StringVar()
        tk.Entry(
            street_frame,
            textvariable=street_var,
            font=("Courier", 10),
            relief="solid",
            bd=1,
        ).pack(side="left", fill="x", expand=True)

        # --- PLUMBER DROPDOWN ---
        plumber_frame = tk.Frame(ticket_frame, bg="white")
        plumber_frame.pack(fill="x", pady=2)
        tk.Label(
            plumber_frame,
            text="Plumber:",
            font=("Courier", 10),
            bg="white",
            width=10,
            anchor="w",
        ).pack(side="left")

        plumber_options: List[str] = get_all_tubero_names()
        if not plumber_options:
            plumber_options = ["Unassigned"]

        plumber_var = tk.StringVar(value=plumber_options[0])
        tk.OptionMenu(plumber_frame, plumber_var, *plumber_options).pack(
            side="left", fill="x", expand=True
        )

        tk.Label(
            ticket_frame,
            text="=========================",
            font=("Courier", 12, "bold"),
            bg="white",
        ).pack(pady=(10, 0))

        def execute_open_case() -> None:
            selected_display_text: str = location_name_var.get()
            selected_id: Optional[int] = loc_map.get(selected_display_text)
            selected_loc_row: Optional[Dict[str, Any]] = next(
                (r for r in self.lv.location_rows if r["id"] == selected_id), None
            )

            selected_problem: str = problem_var.get()
            street_val: str = street_var.get().strip()
            plumber_val: str = plumber_var.get()

            # Execute the case creation/update
            incident_id = open_incident_case(
                post_id=post_id,
                location_row=selected_loc_row,
                intent_word=selected_problem,
                street_name=street_val if street_val else None,
                plumber_name=plumber_val,
            )

            if incident_id:
                self.print_incident_ticket(post_id)

            popup.destroy()
            self.refresh()

        tk.Button(
            popup,
            text="Open Case & Dispatch",
            bg="#3498db",
            fg="white",
            font=("Arial", 12, "bold"),
            command=execute_open_case,
        ).pack(pady=(0, 15))
