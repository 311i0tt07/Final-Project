import tkinter as tk
from tkinter import messagebox
from database_handler import DatabaseHandler
from volunteer import Volunteer
from volunteer_hours import VolunteerHours

class VolunteerApp:
    def __init__(self, root):
        self.db_handler = DatabaseHandler()
        self.root = root
        self.root.title("Volunteer Tracking System")
        self.standardize_ui()
        self.create_main_menu()

    def standardize_ui(self):
        self.bg_color = "lightblue"
        self.font = ("Arial", 12)
        self.button_style = {"bg": "white", "fg": "black", "font": self.font, "padx": 10, "pady": 5, "relief": tk.RAISED}
        self.label_style = {"bg": self.bg_color, "font": self.font}
        self.root.configure(bg=self.bg_color)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()

    def create_main_menu(self):
        self.clear_frame()
        frame = tk.Frame(self.root, bg=self.bg_color)
        frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(frame, text="Main Menu", font=('Helvetica', 16, 'bold'), bg=self.bg_color).pack(pady=20)

        tk.Button(frame, text="Add Volunteer", command=self.add_volunteer_menu, **self.button_style).pack(fill=tk.X, pady=5)
        tk.Button(frame, text="Update Volunteer", command=self.update_volunteer_menu, **self.button_style).pack(fill=tk.X, pady=5)
        tk.Button(frame, text="Remove Volunteer", command=self.remove_volunteer_menu, **self.button_style).pack(fill=tk.X, pady=5)
        tk.Button(frame, text="Log Hours", command=self.log_hours_menu, **self.button_style).pack(fill=tk.X, pady=5)
        tk.Button(frame, text="Generate Reports", command=self.generate_reports_menu, **self.button_style).pack(fill=tk.X, pady=5)
        tk.Button(frame, text="Exit", command=self.exit_app, **self.button_style).pack(fill=tk.X, pady=5)

    def add_volunteer_menu(self):
        self.clear_frame()
        frame = tk.Frame(self.root, bg=self.bg_color)
        frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(frame, text="Add New Volunteer", font=('Helvetica', 16, 'bold'), bg=self.bg_color).pack(pady=20)

        tk.Label(frame, text="ID:", **self.label_style).pack(pady=5)
        id_entry = tk.Entry(frame)
        id_entry.pack(pady=5)

        tk.Label(frame, text="Name:", **self.label_style).pack(pady=5)
        name_entry = tk.Entry(frame)
        name_entry.pack(pady=5)

        tk.Label(frame, text="Email:", **self.label_style).pack(pady=5)
        email_entry = tk.Entry(frame)
        email_entry.pack(pady=5)

        tk.Label(frame, text="Contact Info:", **self.label_style).pack(pady=5)
        contact_entry = tk.Entry(frame)
        contact_entry.pack(pady=5)

        tk.Label(frame, text="Skills (comma-separated):", **self.label_style).pack(pady=5)
        skills_entry = tk.Entry(frame)
        skills_entry.pack(pady=5)

        save_button = tk.Button(frame, text="Save", command=lambda: self.save_new_volunteer(id_entry.get(), name_entry.get(), email_entry.get(), contact_entry.get(), skills_entry.get()), **self.button_style)
        save_button.pack(pady=5)

        back_button = tk.Button(frame, text="Back", command=self.create_main_menu, **self.button_style)
        back_button.pack(pady=5)

    def save_new_volunteer(self, id, name, email, contact_info, skills):
        if not self.validate_not_empty(id, name, email, contact_info, skills):
            messagebox.showerror("Error", "All fields are required!")
            return

        if not self.validate_email(email):
            messagebox.showerror("Error", "Invalid email format!")
            return

        volunteer = Volunteer(id, name, email, contact_info, skills.split(','))
        self.db_handler.add_volunteer(volunteer)
        messagebox.showinfo("Success", "Volunteer added successfully!")
        self.create_main_menu()

    def update_volunteer_menu(self):
        self.clear_frame()
        frame = tk.Frame(self.root, bg=self.bg_color)
        frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(frame, text="Update Volunteer", font=('Helvetica', 16, 'bold'), bg=self.bg_color).pack(pady=20)

        tk.Label(frame, text="Enter ID of Volunteer to Update:", **self.label_style).pack()
        id_entry = tk.Entry(frame)
        id_entry.pack()

        search_button = tk.Button(frame, text="Search", command=lambda: self.search_volunteer(id_entry.get()), **self.button_style)
        search_button.pack()

        back_button = tk.Button(frame, text="Back", command=self.create_main_menu, **self.button_style)
        back_button.pack(pady=5)

    def search_volunteer(self, id):
        volunteer = self.db_handler.get_volunteer_by_id(id)
        if volunteer:
            self.update_volunteer_details(volunteer)
        else:
            messagebox.showerror("Error", "Volunteer not found!")

    def update_volunteer_details(self, volunteer):
        self.clear_frame()
        frame = tk.Frame(self.root, bg=self.bg_color)
        frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(frame, text="Update Volunteer Details", font=('Helvetica', 16, 'bold'), bg=self.bg_color).pack(pady=20)

        tk.Label(frame, text="Name:", **self.label_style).pack()
        name_entry = tk.Entry(frame)
        name_entry.insert(0, volunteer.name)
        name_entry.pack()

        tk.Label(frame, text="Email:", **self.label_style).pack()
        email_entry = tk.Entry(frame)
        email_entry.insert(0, volunteer.email)
        email_entry.pack()

        tk.Label(frame, text="Contact Info:", **self.label_style).pack()
        contact_entry = tk.Entry(frame)
        contact_entry.insert(0, volunteer.contact_info)
        contact_entry.pack()

        tk.Label(frame, text="Skills (comma-separated):", **self.label_style).pack()
        skills_entry = tk.Entry(frame)
        skills_entry.insert(0, ','.join(volunteer.skills))
        skills_entry.pack()

        save_button = tk.Button(frame, text="Save", command=lambda: self.save_updated_volunteer(volunteer.id, name_entry.get(), email_entry.get(), contact_entry.get(), skills_entry.get()), **self.button_style)
        save_button.pack(pady=10)

        back_button = tk.Button(frame, text="Back", command=self.create_main_menu, **self.button_style)
        back_button.pack(pady=10)

    def save_updated_volunteer(self, id, name, email, contact_info, skills):
        if not self.validate_not_empty(name, email, contact_info, skills):
            messagebox.showerror("Error", "All fields are required!")
            return

        if not self.validate_email(email):
            messagebox.showerror("Error", "Invalid email format!")
            return

        volunteer = Volunteer(id, name, email, contact_info, skills.split(','))
        self.db_handler.update_volunteer(volunteer)
        messagebox.showinfo("Success", "Volunteer updated successfully!")
        self.create_main_menu()

    def remove_volunteer_menu(self):
        self.clear_frame()
        frame = tk.Frame(self.root, bg=self.bg_color)
        frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(frame, text="Remove Volunteer", font=('Helvetica', 16, 'bold'), bg=self.bg_color).pack(pady=20)

        tk.Label(frame, text="Enter ID of Volunteer to Remove:", **self.label_style).pack()
        id_entry = tk.Entry(frame)
        id_entry.pack()

        remove_button = tk.Button(frame, text="Remove", command=lambda: self.remove_volunteer(id_entry.get()), **self.button_style)
        remove_button.pack()

        back_button = tk.Button(frame, text="Back", command=self.create_main_menu, **self.button_style)
        back_button.pack(pady=5)

    def remove_volunteer(self, id):
        volunteer = self.db_handler.get_volunteer_by_id(id)
        if volunteer:
            self.db_handler.remove_volunteer(id)
            messagebox.showinfo("Success", "Volunteer removed successfully!")
            self.create_main_menu()
        else:
            messagebox.showerror("Error", "Volunteer not found!")

    def log_hours_menu(self):
        self.clear_frame()
        frame = tk.Frame(self.root, bg=self.bg_color)
        frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(frame, text="Log Volunteer Hours", font=('Helvetica', 16, 'bold'), bg=self.bg_color).pack(pady=20)

        tk.Label(frame, text="Enter Volunteer ID:", **self.label_style).pack()
        id_entry = tk.Entry(frame)
        id_entry.pack()

        tk.Label(frame, text="Date (YYYY-MM-DD):", **self.label_style).pack()
        date_entry = tk.Entry(frame)
        date_entry.pack()

        tk.Label(frame, text="Hours Worked:", **self.label_style).pack()
        hours_entry = tk.Entry(frame)
        hours_entry.pack()

        tk.Label(frame, text="Description:", **self.label_style).pack()
        description_entry = tk.Entry(frame)
        description_entry.pack()

        log_button = tk.Button(frame, text="Log Hours", command=lambda: self.log_hours(id_entry.get(), date_entry.get(), hours_entry.get(), description_entry.get()), **self.button_style)
        log_button.pack()

        back_button = tk.Button(frame, text="Back", command=self.create_main_menu, **self.button_style)
        back_button.pack(pady=5)

    def log_hours(self, id, date, hours, description):
        volunteer = self.db_handler.get_volunteer_by_id(id)
        if volunteer:
            if not self.validate_not_empty(date, hours, description):
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                hours_worked = float(hours)
            except ValueError:
                messagebox.showerror("Error", "Hours worked must be a number!")
                return

            volunteer_hours = VolunteerHours(date, hours_worked, description)
            self.db_handler.add_volunteer_hours(id, volunteer_hours)
            messagebox.showinfo("Success", "Volunteer hours logged successfully!")
            self.create_main_menu()
        else:
            messagebox.showerror("Error", "Volunteer not found!")

    def generate_reports_menu(self):
        self.clear_frame()
        frame = tk.Frame(self.root, bg=self.bg_color)
        frame.pack(expand=True, fill=tk.BOTH)

        tk.Label(frame, text="Generate Reports", font=('Helvetica', 16, 'bold'), bg=self.bg_color).pack(pady=20)

        tk.Button(frame, text="Generate Volunteer Hours Report", command=self.generate_hours_report, **self.button_style).pack(pady=5)
        tk.Button(frame, text="Generate Volunteer Summary Report", command=self.generate_summary_report, **self.button_style).pack(pady=5)

        back_button = tk.Button(frame, text="Back", command=self.create_main_menu, **self.button_style)
        back_button.pack(pady=5)

    def generate_hours_report(self):
        report = self.db_handler.generate_hours_report()
        self.display_report(report)

    def generate_summary_report(self):
        report = self.db_handler.generate_volunteer_summary()
        self.display_report(report)

    def display_report(self, report):
        self.clear_frame()
        frame = tk.Frame(self.root)
        frame.pack(expand=True, fill=tk.BOTH)

        report_text = tk.Text(frame, wrap=tk.WORD)
        report_text.insert(tk.END, report)
        report_text.pack(expand=True, fill=tk.BOTH)

        back_button = tk.Button(frame, text="Back", command=self.create_main_menu, **self.button_style)
        back_button.pack(pady=5)

    def exit_app(self):
        self.db_handler.close()
        self.root.quit()

    def validate_not_empty(self, *args):
        for arg in args:
            if not arg:
                return False
        return True

    def validate_email(self, email):
        import re
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None
