import tkinter as tk
from tkinter import messagebox
import sqlite3
import os

class Volunteer:
    def __init__(self, id, name, email, contact_info, skills):
        self.id = id
        self.name = name
        self.email = email
        self.contact_info = contact_info
        self.skills = skills
        self.hours = []

    def add_hours(self, volunteer_hours):
        self.hours.append(volunteer_hours)

    def update_profile(self, name=None, email=None, contact_info=None, skills=None):
        if name:
            self.name = name
        if email:
            self.email = email
        if contact_info:
            self.contact_info = contact_info
        if skills:
            self.skills = skills

class VolunteerHours:
    def __init__(self, date, hours_worked, description):
        self.date = date
        self.hours_worked = hours_worked
        self.description = description

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def check_password(self, password):
        return self.password == password

class DatabaseHandler:
    def __init__(self, db_file='volunteers.db'):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(script_dir, db_file)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS volunteers (
                id TEXT PRIMARY KEY,
                name TEXT,
                email TEXT,
                contact_info TEXT,
                skills TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS volunteer_hours (
                volunteer_id TEXT,
                date TEXT,
                hours_worked REAL,
                description TEXT,
                FOREIGN KEY (volunteer_id) REFERENCES volunteers(id)
            )
        ''')
        self.conn.commit()

    def add_volunteer(self, volunteer):
        self.cursor.execute('''
            INSERT INTO volunteers (id, name, email, contact_info, skills)
            VALUES (?, ?, ?, ?, ?)
        ''', (volunteer.id, volunteer.name, volunteer.email, volunteer.contact_info, ','.join(volunteer.skills)))
        self.conn.commit()

    def update_volunteer(self, volunteer):
        self.cursor.execute('''
            UPDATE volunteers 
            SET name=?, email=?, contact_info=?, skills=?
            WHERE id=?
        ''', (volunteer.name, volunteer.email, volunteer.contact_info, ','.join(volunteer.skills), volunteer.id))
        self.conn.commit()

    def remove_volunteer(self, volunteer_id):
        self.cursor.execute('''
            DELETE FROM volunteers
            WHERE id=?
        ''', (volunteer_id,))
        self.conn.commit()

    def add_volunteer_hours(self, volunteer_id, hours):
        self.cursor.execute('''
            INSERT INTO volunteer_hours (volunteer_id, date, hours_worked, description)
            VALUES (?, ?, ?, ?)
        ''', (volunteer_id, hours.date, hours.hours_worked, hours.description))
        self.conn.commit()

    def get_all_volunteers(self):
        self.cursor.execute('SELECT * FROM volunteers')
        rows = self.cursor.fetchall()
        volunteers = []
        for row in rows:
            id, name, email, contact_info, skills = row
            volunteer = Volunteer(id, name, email, contact_info, skills.split(','))
            volunteers.append(volunteer)
        return volunteers

    def get_volunteer_by_id(self, volunteer_id):
        self.cursor.execute('SELECT * FROM volunteers WHERE id=?', (volunteer_id,))
        row = self.cursor.fetchone()
        if row:
            id, name, email, contact_info, skills = row
            return Volunteer(id, name, email, contact_info, skills.split(','))
        return None

    def generate_hours_report(self):
        self.cursor.execute('''
            SELECT v.name, SUM(vh.hours_worked) AS total_hours
            FROM volunteers v
            LEFT JOIN volunteer_hours vh ON v.id = vh.volunteer_id
            GROUP BY v.name
        ''')
        rows = self.cursor.fetchall()
        report = "Volunteer Hours Report:\n"
        for row in rows:
            name, total_hours = row
            report += f"{name}: {total_hours} hours\n"
        return report

    def generate_volunteer_summary(self):
        self.cursor.execute('SELECT * FROM volunteers')
        rows = self.cursor.fetchall()
        report = "Volunteer Summary Report:\n"
        for row in rows:
            id, name, email, contact_info, skills = row
            report += f"ID: {id}, Name: {name}, Email: {email}, Contact: {contact_info}, Skills: {skills}\n"
        return report

    def close(self):
        self.conn.close()

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

        search_button = tk.Button(frame, text="Search", command=lambda:

 self.search_volunteer(id_entry.get()), **self.button_style)
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

def main():
    root = tk.Tk()
    app = VolunteerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
