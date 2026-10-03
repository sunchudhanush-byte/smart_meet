import tkinter as tk
from tkinter import messagebox, ttk

from algorithm import (
    find_common_free_intervals,
    generate_meeting_slots
)


class SmartMeetGUI:

    # =========================================================
    # COLORS
    # =========================================================

    BG_COLOR = "#F4F7FB"
    CARD_COLOR = "#FFFFFF"

    PRIMARY = "#2563EB"
    PRIMARY_DARK = "#1D4ED8"

    SUCCESS = "#16A34A"
    SUCCESS_DARK = "#15803D"

    DANGER = "#DC2626"
    DANGER_DARK = "#B91C1C"

    WARNING = "#F59E0B"

    TEXT_DARK = "#172033"
    TEXT_GRAY = "#64748B"

    LIGHT_BLUE = "#E8F0FE"
    LIGHT_GREEN = "#EAF8EF"
    LIGHT_RED = "#FEECEC"

    # =========================================================
    # INITIALIZATION
    # =========================================================

    def __init__(self, root):

        self.root = root

        self.root.title(
            "SMARTMEET - Common Meeting Time Finder"
        )

        # Increased window height so results are visible
        self.root.geometry("1100x850")

        self.root.minsize(
            950,
            700
        )

        self.root.configure(
            bg=self.BG_COLOR
        )

        self.participants = {}

        self.meeting_slots = []

        self.setup_styles()

        self.create_header()

        self.create_settings_card()

        self.create_schedule_card()

        self.create_results_card()

        self.create_status_bar()

        self.update_status(
            "Ready — add participant schedules to begin."
        )

    # =========================================================
    # STYLES
    # =========================================================

    def setup_styles(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Treeview",
            background="white",
            foreground=self.TEXT_DARK,
            rowheight=32,
            fieldbackground="white",
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            background=self.PRIMARY,
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=8
        )

        style.map(
            "Treeview",
            background=[
                ("selected", "#DBEAFE")
            ],
            foreground=[
                ("selected", self.TEXT_DARK)
            ]
        )

    # =========================================================
    # HEADER
    # =========================================================

    def create_header(self):

        header = tk.Frame(
            self.root,
            bg=self.PRIMARY,
            height=115
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(
            False
        )

        title = tk.Label(
            header,
            text="SMARTMEET",
            font=("Segoe UI", 28, "bold"),
            bg=self.PRIMARY,
            fg="white"
        )

        title.pack(
            pady=(18, 0)
        )

        subtitle = tk.Label(
            header,
            text="Find the perfect common meeting time",
            font=("Segoe UI", 12),
            bg=self.PRIMARY,
            fg="#DBEAFE"
        )

        subtitle.pack(
            pady=(2, 0)
        )

    # =========================================================
    # MEETING SETTINGS
    # =========================================================

    def create_settings_card(self):

        card = tk.Frame(
            self.root,
            bg=self.CARD_COLOR,
            bd=0,
            highlightthickness=1,
            highlightbackground="#E2E8F0"
        )

        card.pack(
            fill="x",
            padx=25,
            pady=(20, 10)
        )

        title = tk.Label(
            card,
            text="⚙  MEETING SETTINGS",
            font=("Segoe UI", 12, "bold"),
            bg=self.CARD_COLOR,
            fg=self.TEXT_DARK
        )

        title.grid(
            row=0,
            column=0,
            columnspan=8,
            sticky="w",
            padx=20,
            pady=(15, 12)
        )

        self.create_label(
            card,
            "Working Start",
            1,
            0
        )

        self.work_start_entry = self.create_entry(
            card,
            1,
            1,
            "09:00"
        )

        self.create_label(
            card,
            "Working End",
            1,
            2
        )

        self.work_end_entry = self.create_entry(
            card,
            1,
            3,
            "17:00"
        )

        self.create_label(
            card,
            "Meeting Duration",
            1,
            4
        )

        self.duration_entry = self.create_entry(
            card,
            1,
            5,
            "30"
        )

        duration_label = tk.Label(
            card,
            text="minutes",
            font=("Segoe UI", 10),
            bg=self.CARD_COLOR,
            fg=self.TEXT_GRAY
        )

        duration_label.grid(
            row=1,
            column=6,
            padx=(0, 20),
            pady=(0, 15)
        )

        info = tk.Label(
            card,
            text="Use 24-hour format (HH:MM)",
            font=("Segoe UI", 9),
            bg=self.CARD_COLOR,
            fg=self.TEXT_GRAY
        )

        info.grid(
            row=2,
            column=0,
            columnspan=7,
            sticky="w",
            padx=20,
            pady=(0, 15)
        )

    # =========================================================
    # PARTICIPANT SCHEDULE CARD
    # =========================================================

    def create_schedule_card(self):

        card = tk.Frame(
            self.root,
            bg=self.CARD_COLOR,
            bd=0,
            highlightthickness=1,
            highlightbackground="#E2E8F0"
        )

        card.pack(
            fill="x",
            padx=25,
            pady=10
        )

        title = tk.Label(
            card,
            text="👥  ADD PARTICIPANT SCHEDULE",
            font=("Segoe UI", 12, "bold"),
            bg=self.CARD_COLOR,
            fg=self.TEXT_DARK
        )

        title.grid(
            row=0,
            column=0,
            columnspan=8,
            sticky="w",
            padx=20,
            pady=(15, 12)
        )

        # -----------------------------------------------------
        # Participant
        # -----------------------------------------------------

        self.create_label(
            card,
            "Participant",
            1,
            0
        )

        self.name_entry = self.create_entry(
            card,
            1,
            1,
            ""
        )

        self.name_entry.configure(
            width=18
        )

        # -----------------------------------------------------
        # Busy From
        # -----------------------------------------------------

        self.create_label(
            card,
            "Busy From",
            1,
            2
        )

        self.busy_start_entry = self.create_entry(
            card,
            1,
            3,
            ""
        )

        # -----------------------------------------------------
        # Busy Until
        # -----------------------------------------------------

        self.create_label(
            card,
            "Busy Until",
            1,
            4
        )

        self.busy_end_entry = self.create_entry(
            card,
            1,
            5,
            ""
        )

        # -----------------------------------------------------
        # Add Schedule Button
        # -----------------------------------------------------

        add_button = tk.Button(
            card,
            text="＋  Add Schedule",
            command=self.add_schedule,
            bg=self.PRIMARY,
            fg="white",
            activebackground=self.PRIMARY_DARK,
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            padx=15,
            pady=8,
            cursor="hand2"
        )

        add_button.grid(
            row=1,
            column=6,
            padx=15,
            pady=5
        )

        self.add_hover_effect(
            add_button,
            self.PRIMARY,
            self.PRIMARY_DARK
        )

        # -----------------------------------------------------
        # Schedule Table
        # Reduced height from 5 to 3
        # -----------------------------------------------------

        table_frame = tk.Frame(
            card,
            bg=self.CARD_COLOR
        )

        table_frame.grid(
            row=2,
            column=0,
            columnspan=8,
            sticky="ew",
            padx=20,
            pady=(15, 8)
        )

        columns = (
            "participant",
            "start",
            "end"
        )

        self.schedule_table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=3,
            selectmode="browse"
        )

        self.schedule_table.heading(
            "participant",
            text="Participant"
        )

        self.schedule_table.heading(
            "start",
            text="Busy From"
        )

        self.schedule_table.heading(
            "end",
            text="Busy Until"
        )

        self.schedule_table.column(
            "participant",
            width=250,
            anchor="center"
        )

        self.schedule_table.column(
            "start",
            width=180,
            anchor="center"
        )

        self.schedule_table.column(
            "end",
            width=180,
            anchor="center"
        )

        self.schedule_table.pack(
            side="left",
            fill="x",
            expand=True
        )

        table_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.schedule_table.yview
        )

        table_scrollbar.pack(
            side="right",
            fill="y"
        )

        self.schedule_table.configure(
            yscrollcommand=table_scrollbar.set
        )

        # -----------------------------------------------------
        # Bottom Buttons
        # -----------------------------------------------------

        button_frame = tk.Frame(
            card,
            bg=self.CARD_COLOR
        )

        button_frame.grid(
            row=3,
            column=0,
            columnspan=8,
            sticky="w",
            padx=20,
            pady=(2, 15)
        )

        # -----------------------------------------------------
        # DEMO DATA
        # -----------------------------------------------------

        demo_button = tk.Button(
            button_frame,
            text="🎯  Load Demo Data",
            command=self.load_demo_data,
            bg=self.WARNING,
            fg="white",
            activebackground="#D97706",
            activeforeground="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            bd=0,
            padx=15,
            pady=7,
            cursor="hand2"
        )

        demo_button.pack(
            side="left",
            padx=(0, 10)
        )

        self.add_hover_effect(
            demo_button,
            self.WARNING,
            "#D97706"
        )

        # -----------------------------------------------------
        # REMOVE SELECTED
        # -----------------------------------------------------

        remove_button = tk.Button(
            button_frame,
            text="🗑  Remove Selected",
            command=self.remove_selected,
            bg=self.DANGER,
            fg="white",
            activebackground=self.DANGER_DARK,
            activeforeground="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            bd=0,
            padx=15,
            pady=7,
            cursor="hand2"
        )

        remove_button.pack(
            side="left",
            padx=(0, 10)
        )

        self.add_hover_effect(
            remove_button,
            self.DANGER,
            self.DANGER_DARK
        )

        # -----------------------------------------------------
        # CLEAR ALL
        # -----------------------------------------------------

        clear_button = tk.Button(
            button_frame,
            text="🧹  Clear All",
            command=self.clear_all,
            bg="#64748B",
            fg="white",
            activebackground="#475569",
            activeforeground="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            bd=0,
            padx=15,
            pady=7,
            cursor="hand2"
        )

        clear_button.pack(
            side="left"
        )

        self.add_hover_effect(
            clear_button,
            "#64748B",
            "#475569"
        )

        # -----------------------------------------------------
        # COUNTER
        # -----------------------------------------------------

        self.counter_label = tk.Label(
            button_frame,
            text="0 participants • 0 schedules",
            font=("Segoe UI", 9),
            bg=self.CARD_COLOR,
            fg=self.TEXT_GRAY
        )

        self.counter_label.pack(
            side="left",
            padx=20
        )

    # =========================================================
    # RESULTS CARD
    # =========================================================

    def create_results_card(self):

        card = tk.Frame(
            self.root,
            bg=self.CARD_COLOR,
            bd=0,
            highlightthickness=1,
            highlightbackground="#E2E8F0"
        )

        # Give Results the remaining available space
        card.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=10
        )

        # -----------------------------------------------------
        # RESULTS HEADER
        # -----------------------------------------------------

        header_frame = tk.Frame(
            card,
            bg=self.CARD_COLOR
        )

        header_frame.pack(
            fill="x",
            padx=20,
            pady=(15, 5)
        )

        title = tk.Label(
            header_frame,
            text="✨  MEETING RESULTS",
            font=("Segoe UI", 12, "bold"),
            bg=self.CARD_COLOR,
            fg=self.TEXT_DARK
        )

        title.pack(
            side="left"
        )

        # -----------------------------------------------------
        # FIND COMMON TIME
        # -----------------------------------------------------

        find_button = tk.Button(
            header_frame,
            text="🔍  Find Common Time",
            command=self.find_common_time,
            bg=self.SUCCESS,
            fg="white",
            activebackground=self.SUCCESS_DARK,
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            bd=0,
            padx=20,
            pady=9,
            cursor="hand2"
        )

        find_button.pack(
            side="right"
        )

        self.add_hover_effect(
            find_button,
            self.SUCCESS,
            self.SUCCESS_DARK
        )

        # -----------------------------------------------------
        # COMMON AVAILABLE TIMES
        # -----------------------------------------------------

        common_label = tk.Label(
            card,
            text="Common Available Times",
            font=("Segoe UI", 10, "bold"),
            bg=self.CARD_COLOR,
            fg=self.TEXT_DARK
        )

        common_label.pack(
            anchor="w",
            padx=20,
            pady=(8, 5)
        )

        # IMPORTANT:
        # No fixed height now.
        # The frame will size itself according to its content.
        self.common_frame = tk.Frame(
            card,
            bg="#F8FAFC"
        )

        self.common_frame.pack(
            fill="x",
            padx=20,
            pady=(0, 8)
        )

        # Do NOT use pack_propagate(False)
        # This allows the common time cards to remain visible.

        self.common_placeholder = tk.Label(
            self.common_frame,
            text="Your common available times will appear here.",
            font=("Segoe UI", 10),
            bg="#F8FAFC",
            fg=self.TEXT_GRAY
        )

        self.common_placeholder.pack(
            expand=True,
            pady=12
        )

        # -----------------------------------------------------
        # POSSIBLE MEETING SLOTS
        # -----------------------------------------------------

        slots_label = tk.Label(
            card,
            text="📅 Possible Meeting Slots",
            font=("Segoe UI", 10, "bold"),
            bg=self.CARD_COLOR,
            fg=self.TEXT_DARK
        )

        slots_label.pack(
            anchor="w",
            padx=20,
            pady=(5, 5)
        )

        self.slots_frame = tk.Frame(
            card,
            bg=self.CARD_COLOR
        )

        self.slots_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 8)
        )

        self.slots_placeholder = tk.Label(
            self.slots_frame,
            text="Click 'Find Common Time' to generate meeting slots.",
            font=("Segoe UI", 10),
            bg=self.CARD_COLOR,
            fg=self.TEXT_GRAY
        )

        self.slots_placeholder.pack(
            pady=15
        )

        # -----------------------------------------------------
        # SELECTED SLOT
        # -----------------------------------------------------

        self.selected_slot_label = tk.Label(
            card,
            text="No meeting slot selected",
            font=("Segoe UI", 10, "bold"),
            bg=self.LIGHT_BLUE,
            fg=self.PRIMARY
        )

        self.selected_slot_label.pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

    # =========================================================
    # STATUS BAR
    # =========================================================

    def create_status_bar(self):

        self.status_bar = tk.Label(
            self.root,
            text="",
            font=("Segoe UI", 9),
            bg="#E2E8F0",
            fg=self.TEXT_DARK,
            anchor="w",
            padx=15,
            pady=5
        )

        self.status_bar.pack(
            fill="x",
            side="bottom"
        )

    # =========================================================
    # LABEL HELPER
    # =========================================================

    def create_label(
        self,
        parent,
        text,
        row,
        column
    ):

        label = tk.Label(
            parent,
            text=text,
            font=("Segoe UI", 9, "bold"),
            bg=self.CARD_COLOR,
            fg=self.TEXT_GRAY
        )

        label.grid(
            row=row,
            column=column,
            padx=(10, 5),
            pady=5,
            sticky="e"
        )

        return label

    # =========================================================
    # ENTRY HELPER
    # =========================================================

    def create_entry(
        self,
        parent,
        row,
        column,
        default_value
    ):

        entry = tk.Entry(
            parent,
            width=12,
            font=("Segoe UI", 10),
            bg="#F8FAFC",
            fg=self.TEXT_DARK,
            relief="solid",
            bd=1
        )

        entry.grid(
            row=row,
            column=column,
            padx=5,
            pady=5
        )

        if default_value:

            entry.insert(
                0,
                default_value
            )

        return entry

    # =========================================================
    # HOVER EFFECT
    # =========================================================

    def add_hover_effect(
        self,
        button,
        normal_color,
        hover_color
    ):

        button.bind(
            "<Enter>",
            lambda event: button.configure(
                bg=hover_color
            )
        )

        button.bind(
            "<Leave>",
            lambda event: button.configure(
                bg=normal_color
            )
        )

    # =========================================================
    # ADD SCHEDULE
    # =========================================================

    def add_schedule(self):

        name = (
            self.name_entry
            .get()
            .strip()
        )

        busy_start = (
            self.busy_start_entry
            .get()
            .strip()
        )

        busy_end = (
            self.busy_end_entry
            .get()
            .strip()
        )

        if (
            not name
            or not busy_start
            or not busy_end
        ):

            messagebox.showerror(
                "Missing Information",
                "Please enter participant name, "
                "busy start time and busy end time."
            )

            return

        try:

            start_parts = busy_start.split(":")
            end_parts = busy_end.split(":")

            if (
                len(start_parts) != 2
                or len(end_parts) != 2
            ):

                raise ValueError

            start_hour = int(
                start_parts[0]
            )

            start_minute = int(
                start_parts[1]
            )

            end_hour = int(
                end_parts[0]
            )

            end_minute = int(
                end_parts[1]
            )

            if (
                start_hour < 0
                or start_hour > 23
                or start_minute < 0
                or start_minute > 59
            ):

                raise ValueError

            if (
                end_hour < 0
                or end_hour > 23
                or end_minute < 0
                or end_minute > 59
            ):

                raise ValueError

            start_total = (
                start_hour * 60
                + start_minute
            )

            end_total = (
                end_hour * 60
                + end_minute
            )

            if start_total >= end_total:

                messagebox.showerror(
                    "Invalid Schedule",
                    "Busy start time must be before "
                    "busy end time."
                )

                return

        except ValueError:

            messagebox.showerror(
                "Invalid Time",
                "Please enter time using HH:MM format.\n\n"
                "Example: 09:30"
            )

            return

        busy_start = (
            f"{start_hour:02d}:{start_minute:02d}"
        )

        busy_end = (
            f"{end_hour:02d}:{end_minute:02d}"
        )

        if name not in self.participants:

            self.participants[name] = []

        self.participants[name].append(
            (
                busy_start,
                busy_end
            )
        )

        self.schedule_table.insert(
            "",
            tk.END,
            values=(
                name,
                busy_start,
                busy_end
            )
        )

        self.name_entry.delete(
            0,
            tk.END
        )

        self.busy_start_entry.delete(
            0,
            tk.END
        )

        self.busy_end_entry.delete(
            0,
            tk.END
        )

        self.update_counter()

        self.clear_results()

        self.update_status(
            f"Added schedule for {name}."
        )

        self.name_entry.focus()

    # =========================================================
    # LOAD DEMO DATA
    # =========================================================

    def load_demo_data(self):

        # Clear existing schedules

        self.participants.clear()

        self.schedule_table.delete(
            *self.schedule_table.get_children()
        )

        # Demo participant schedules

        demo_schedules = {

            "Alice": [
                ("09:00", "10:00"),
                ("13:00", "14:00")
            ],

            "Bob": [
                ("09:30", "11:00"),
                ("14:00", "15:00")
            ],

            "Charlie": [
                ("10:00", "11:30")
            ],

            "David": [
                ("12:30", "13:30"),
                ("16:00", "16:30")
            ]
        }

        # Store schedules

        self.participants.update(
            demo_schedules
        )

        # Display schedules

        for person, intervals in (
            demo_schedules.items()
        ):

            for start, end in intervals:

                self.schedule_table.insert(
                    "",
                    tk.END,
                    values=(
                        person,
                        start,
                        end
                    )
                )

        self.update_counter()

        self.clear_results()

        self.update_status(
            "Demo data loaded — ready to find common time."
        )

    # =========================================================
    # REMOVE SELECTED
    # =========================================================

    def remove_selected(self):

        selected = (
            self.schedule_table.selection()
        )

        if not selected:

            messagebox.showwarning(
                "No Selection",
                "Please select a schedule from the table."
            )

            return

        item_id = selected[0]

        values = self.schedule_table.item(
            item_id,
            "values"
        )

        name = values[0]
        start = values[1]
        end = values[2]

        if name in self.participants:

            try:

                self.participants[name].remove(
                    (
                        start,
                        end
                    )
                )

            except ValueError:

                pass

            if not self.participants[name]:

                del self.participants[name]

        self.schedule_table.delete(
            item_id
        )

        self.update_counter()

        self.clear_results()

        self.update_status(
            f"Removed {name}'s schedule."
        )

    # =========================================================
    # CLEAR ALL
    # =========================================================

    def clear_all(self):

        if not self.participants:

            self.update_status(
                "There are no schedules to clear."
            )

            return

        answer = messagebox.askyesno(
            "Clear All Schedules",
            "Are you sure you want to remove all schedules?"
        )

        if not answer:

            return

        self.participants.clear()

        self.schedule_table.delete(
            *self.schedule_table.get_children()
        )

        self.clear_results()

        self.update_counter()

        self.update_status(
            "All schedules have been cleared."
        )

    # =========================================================
    # FIND COMMON TIME
    # =========================================================

    def find_common_time(self):

        if not self.participants:

            messagebox.showerror(
                "No Schedules",
                "Please add at least one participant "
                "schedule first."
            )

            return

        work_start = (
            self.work_start_entry
            .get()
            .strip()
        )

        work_end = (
            self.work_end_entry
            .get()
            .strip()
        )

        duration_text = (
            self.duration_entry
            .get()
            .strip()
        )

        try:

            meeting_duration = int(
                duration_text
            )

            if meeting_duration <= 0:

                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Duration",
                "Meeting duration must be a "
                "positive whole number."
            )

            return

        try:

            result = find_common_free_intervals(
                self.participants,
                work_start,
                work_end,
                meeting_duration
            )

            self.meeting_slots = (
                generate_meeting_slots(
                    result,
                    meeting_duration
                )
            )

        except ValueError as error:

            messagebox.showerror(
                "Input Error",
                str(error)
            )

            return

        except Exception as error:

            messagebox.showerror(
                "Unexpected Error",
                str(error)
            )

            return

        # Display results

        self.display_common_times(
            result
        )

        self.display_meeting_slots()

        if result:

            self.update_status(
                f"Found {len(result)} common "
                f"available period(s) and "
                f"{len(self.meeting_slots)} "
                f"meeting slot(s)."
            )

        else:

            self.update_status(
                "No common meeting time was found."
            )

    # =========================================================
    # DISPLAY COMMON TIMES
    # =========================================================

    def display_common_times(
        self,
        result
    ):

        # Remove old widgets

        for widget in (
            self.common_frame.winfo_children()
        ):

            widget.destroy()

        if not result:

            label = tk.Label(
                self.common_frame,
                text="❌ No common available time found",
                font=("Segoe UI", 11, "bold"),
                bg=self.LIGHT_RED,
                fg=self.DANGER
            )

            label.pack(
                fill="x",
                padx=10,
                pady=10
            )

            return

        # Display each common interval

        for index, (
            start,
            end,
            duration
        ) in enumerate(result):

            interval_frame = tk.Frame(
                self.common_frame,
                bg=self.LIGHT_GREEN,
                bd=1,
                relief="solid"
            )

            # Reduced padding to keep everything visible

            interval_frame.pack(
                side="left",
                fill="both",
                expand=True,
                padx=5,
                pady=5
            )

            time_label = tk.Label(
                interval_frame,
                text=f"✓  {start} - {end}",
                font=("Segoe UI", 11, "bold"),
                bg=self.LIGHT_GREEN,
                fg=self.SUCCESS
            )

            time_label.pack(
                pady=(6, 2)
            )

            duration_label = tk.Label(
                interval_frame,
                text=f"{duration} minutes available",
                font=("Segoe UI", 9),
                bg=self.LIGHT_GREEN,
                fg=self.TEXT_GRAY
            )

            duration_label.pack(
                pady=(0, 6)
            )

    # =========================================================
    # DISPLAY MEETING SLOTS
    # =========================================================

    def display_meeting_slots(self):

        for widget in (
            self.slots_frame.winfo_children()
        ):

            widget.destroy()

        if not self.meeting_slots:

            label = tk.Label(
                self.slots_frame,
                text="❌ No meeting slots available",
                font=("Segoe UI", 10, "bold"),
                bg=self.CARD_COLOR,
                fg=self.DANGER
            )

            label.pack(
                pady=15
            )

            return

        columns_per_row = 4

        for index, (
            start,
            end
        ) in enumerate(
            self.meeting_slots
        ):

            row = (
                index
                // columns_per_row
            )

            column = (
                index
                % columns_per_row
            )

            slot_button = tk.Button(
                self.slots_frame,
                text=f"🕐 {start} - {end}",
                command=lambda s=start, e=end:
                    self.select_meeting_slot(
                        s,
                        e
                    ),
                bg=self.LIGHT_BLUE,
                fg=self.PRIMARY,
                activebackground="#BFDBFE",
                activeforeground=self.PRIMARY_DARK,
                font=("Segoe UI", 10, "bold"),
                relief="flat",
                bd=0,
                padx=15,
                pady=10,
                cursor="hand2"
            )

            slot_button.grid(
                row=row,
                column=column,
                padx=6,
                pady=6,
                sticky="ew"
            )

            self.add_hover_effect(
                slot_button,
                self.LIGHT_BLUE,
                "#BFDBFE"
            )

        for column in range(
            columns_per_row
        ):

            self.slots_frame.grid_columnconfigure(
                column,
                weight=1
            )

    # =========================================================
    # SELECT MEETING SLOT
    # =========================================================

    def select_meeting_slot(
        self,
        start,
        end
    ):

        self.selected_slot_label.configure(
            text=(
                f"✓  Selected Meeting Slot: "
                f"{start} - {end}"
            ),
            bg=self.LIGHT_GREEN,
            fg=self.SUCCESS
        )

        self.update_status(
            f"Meeting slot selected: "
            f"{start} - {end}"
        )

        messagebox.showinfo(
            "Meeting Slot Selected",
            f"Selected meeting time:\n\n"
            f"{start} - {end}\n\n"
            f"This slot is available for all participants."
        )

    # =========================================================
    # CLEAR RESULTS
    # =========================================================

    def clear_results(self):

        # Clear common times

        for widget in (
            self.common_frame.winfo_children()
        ):

            widget.destroy()

        placeholder = tk.Label(
            self.common_frame,
            text="Your common available times will appear here.",
            font=("Segoe UI", 10),
            bg="#F8FAFC",
            fg=self.TEXT_GRAY
        )

        placeholder.pack(
            pady=12
        )

        # Clear meeting slots

        for widget in (
            self.slots_frame.winfo_children()
        ):

            widget.destroy()

        placeholder = tk.Label(
            self.slots_frame,
            text="Click 'Find Common Time' to generate meeting slots.",
            font=("Segoe UI", 10),
            bg=self.CARD_COLOR,
            fg=self.TEXT_GRAY
        )

        placeholder.pack(
            pady=15
        )

        # Reset selected slot

        self.selected_slot_label.configure(
            text="No meeting slot selected",
            bg=self.LIGHT_BLUE,
            fg=self.PRIMARY
        )

        self.meeting_slots = []

    # =========================================================
    # UPDATE COUNTER
    # =========================================================

    def update_counter(self):

        participant_count = len(
            self.participants
        )

        schedule_count = sum(
            len(intervals)
            for intervals in (
                self.participants.values()
            )
        )

        self.counter_label.configure(
            text=(
                f"{participant_count} participant"
                f"{'s' if participant_count != 1 else ''}"
                f" • "
                f"{schedule_count} schedule"
                f"{'s' if schedule_count != 1 else ''}"
            )
        )

    # =========================================================
    # UPDATE STATUS
    # =========================================================

    def update_status(
        self,
        message
    ):

        self.status_bar.configure(
            text=f"  ●  {message}"
        )


# =============================================================
# PROGRAM ENTRY POINT
# =============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = SmartMeetGUI(
        root
    )

    root.mainloop()