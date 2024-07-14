import tkinter as tk
from tkinter import messagebox
import os
import re

class Volunteer:
    def __init__(self, id, name, email, contact_info, skills):
        # Initialize a Volunteer object with the given attributes
        self.id = id
        self.name = name
        self.email = email
        self.contact_info = contact_info
        self.skills = skills
        self.hours = []

    def add_hours(self, volunteer_hours):
        # Add hours worked by the volunteer
        self.hours.append(volunteer_hours)

    def update_profile(self, name=None, email=None, contact_info=None, skills=None):
        # Update volunteer profile with new information
        if name:
            self.name = name
        if email:
            self.email = email
        if contact_info:
            self.contact_info = contact_info
        if skills:
            self.skills = skills

    def __str__(self):
        # Return a string representation of the volunteer
        return f"ID: {self.id}, Name: {self.name}, Email: {self.email}, Contact: {self.contact_info}, Skills: {', '.join(self.skills)}"

    def save_to_file(self):
        # Save volunteer information to a text file
        with open(f"{self.id}.txt", 'w') as f:
            f.write(f"{self.id}\n")
            f.write(f"{self.name}\n")
            f.write(f"{self.email}\n")
            f.write(f"{self.contact_info}\n")
            f.write(f"{','.join(self.skills)}\n")
            for h in self.hours:
                f.write(f"{h.date},{h.hours_worked},{h.description}\n")

    @staticmethod
    def load_from_file(file_path):
        # Load volunteer information from a text file
        with open(file_path, 'r') as f:
            id = f.readline().strip()
            name = f.readline().strip()
            email = f.readline().strip()
            contact_info = f.readline().strip()
            skills = f.readline().strip().split(',')
            volunteer = Volunteer(id, name, email, contact_info, skills)
            for line in f.readlines():
                date, hours_worked, description = line.strip().split(',')
                volunteer.add_hours(VolunteerHours(date, float(hours_worked), description))
            return volunteer

class VolunteerHours:
    def __init__(self, date, hours_worked, description):
        # Initialize a VolunteerHours object with the given attributes
        self.date = date
        self.hours_worked = hours_worked
        self.description = description

    def __str__(self):
        # Return a string representation of the volunteer hours
        return f"Date: {self.date}, Hours Worked: {self.hours_worked}, Description: {self.description}"

class User:
    def __init__(self, username, password):
        # Initialize a User object with the given attributes
        self.username = username
        self.password = password

    def check_password(self, password):
        # Check if the provided password matches the user's password
        return self.password == password

class Administrator:
    def __init__(self):
        # Initialize an Administrator object with an empty dictionary of volunteers
        self.volunteers = {}

    def add_volunteer(self, volunteer):
        # Add a volunteer to the dictionary
        self.volunteers[volunteer.id] = volunteer

    def remove_volunteer(self, volunteer_id):
        # Remove a volunteer from the dictionary
        if volunteer_id in self.volunteers:
            del self.volunteers[volunteer_id]

    def update_volunteer(self, volunteer_id, **kwargs):
        # Update a volunteer's information
        if volunteer_id in self.volunteers:
            volunteer = self.volunteers[volunteer_id]
            volunteer.update_profile(**kwargs)

    def get_volunteer(self, volunteer_id):
        # Retrieve a volunteer by their ID
        return self.volunteers.get(volunteer_id)

    def save_all_volunteers(self):
        # Save all volunteers to their respective text files
        for volunteer in self.volunteers.values():
            volunteer.save_to_file()

    def load_all_volunteers(self, directory):
        # Load all volunteers from text files in a given directory
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                volunteer = Volunteer.load_from_file(os.path.join(directory, filename))
                self.add_volunteer(volunteer)

    def __str__(self):
        # Return a string representation of all volunteers
        return f"Volunteers: {[str(v) for v in self.volunteers.values()]}"

class Reports:
    def generate_hours_report(self, manager):
        # Generate a report of total hours worked by each volunteer
        report = "Volunteer Hours Report:\n"
        for volunteer in manager.volunteers.values():
            total_hours = sum(log.hours_worked for log in volunteer.hours)
            report += f"{volunteer.name}: {total_hours} hours\n"
        return report

    def generate_volunteer_summary(self, manager):
        # Generate a summary report of all volunteers
        report = "Volunteer Summary Report:\n"
        for volunteer in manager.volunteers.values():
            report += f"{volunteer}\n"
        return report

class VolunteerApp:
    def __init__(self, root):
        # Initialize the VolunteerApp with the root window and create the main menu
        self.admin = Administrator()
        self.reports = Reports()
        self.root = root
        self.root.title("Volunteer Tracking System")
        self.create_main_menu()

    def create_main_menu(self):
        # Create the main menu with buttons for different actions
        self.main_frame = tk.Frame(self.root, bg="lightblue", padx=10, pady=10)
        self.main_frame.pack(expand=True, fill=tk.BOTH)

        button_style = {"bg": "white", "fg": "black", "font": ("Arial", 12), "padx": 10, "pady": 5, "relief": tk.RAISED}

        tk.Button(self.main_frame, text="Add Volunteer", command=self.add_volunteer, **button_style).pack(fill=tk.X, pady=5)
        tk.Button(self.main_frame, text="Update Volunteer", command=self.update_volunteer, **button_style).pack(fill=tk.X, pady=5)
        tk.Button(self.main_frame, text="Remove Volunteer", command=self.remove_volunteer, **button_style).pack(fill=tk.X, pady=5)
        tk.Button(self.main_frame, text="Log Hours", command=self.log_hours, **button_style).pack(fill=tk.X, pady=5)
        tk.Button(self.main_frame, text="Search Volunteers", command=self.search_volunteers, **button_style).pack(fill=tk.X, pady=5)
        tk.Button(self.main_frame, text="Generate Reports", command=self.generate_reports, **button_style).pack(fill=tk.X, pady=5)
        tk.Button(self.main_frame, text="Exit", command=self.exit_app, **button_style).pack(fill=tk.X, pady=5)

    def validate_email(self, email):
        # Validate that the email follows a basic pattern
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def validate_date(self, date):
        # Validate that the date follows the YYYY-MM-DD format
        return re.match(r"\d{4}-\d{2}-\d{2}", date)

    def validate_hours(self, hours):
        # Validate that the hours worked is a positive number
        try:
            hours = float(hours)
            return hours > 0
        except ValueError:
            return False

    def validate_not_empty(self, *args):
        # Validate that all provided fields are not empty
        return all(args)

    def add_volunteer(self):
        # Clear the frame and show the form to add a new volunteer
        self.clear_frame()
        self.volunteer_form("Add Volunteer", self.save_new_volunteer)

    def save_new_volunteer(self):
        # Save the new volunteer information
        id = self.id_entry.get()
        name = self.name_entry.get()
        email = self.email_entry.get()
        contact_info = self.contact_entry.get()
        skills = self.skills_entry.get().split(',')

        # Validate user input
        if not self.validate_not_empty(id, name, email, contact_info, skills):
            messagebox.showerror("Error", "All fields are required!")
            return

        if not self.validate_email(email):
            messagebox.showerror("Error", "Invalid email format!")
            return

        volunteer = Volunteer(id, name, email, contact_info, skills)
        self.admin.add_volunteer(volunteer)
        volunteer.save_to_file()
        messagebox.showinfo("Success", "Volunteer added successfully!")
        self.create_main_menu()

    def update_volunteer(self):
        # Clear the frame and show the form to update an existing volunteer
        self.clear_frame()
        self.volunteer_form("Update Volunteer", self.save_updated_volunteer)

    def save_updated_volunteer(self):
        # Save the updated volunteer information
        id = self.id_entry.get()
        volunteer = self.admin.get_volunteer(id)
        if volunteer:
            name = self.name_entry.get()
            email = self.email_entry.get()
            contact_info = self.contact_entry.get()
            skills = self.skills_entry.get().split(',')

            # Validate user input
            if not self.validate_not_empty(id, name, email, contact_info, skills):
                messagebox.showerror("Error", "All fields are required!")
                return

            if not self.validate_email(email):
                messagebox.showerror("Error", "Invalid email format!")
                return

            self.admin.update_volunteer(id, name=name, email=email, contact_info=contact_info, skills=skills)
            volunteer.save_to_file()
            messagebox.showinfo("Success", "Volunteer updated successfully!")
        else:
            messagebox.showerror("Error", "Volunteer not found!")
        self.create_main_menu()

    def remove_volunteer(self):
        # Clear the frame and show the form to remove a volunteer
        self.clear_frame()
        tk.Label(self.root, text="Enter Volunteer ID to remove:").pack()
        id_entry = tk.Entry(self.root)
        id_entry.pack()
        tk.Button(self.root, text="Remove", command=lambda: self.delete_volunteer(id_entry.get())).pack()

    def delete_volunteer(self, volunteer_id):
        # Remove the volunteer and delete the corresponding file
        self.admin.remove_volunteer(volunteer_id)
        try:
            os.remove(f"{volunteer_id}.txt")
        except FileNotFoundError:
            pass
        messagebox.showinfo("Success", "Volunteer removed successfully!")
        self.create_main_menu()

    def log_hours(self):
        # Clear the frame and show the form to log hours for a volunteer
        self.clear_frame()
        tk.Label(self.root, text="Enter Volunteer ID to log hours for:").pack()
        self.log_id_entry = tk.Entry(self.root)
        self.log_id_entry.pack()
        tk.Label(self.root, text="Enter Date (YYYY-MM-DD):").pack()
        self.log_date_entry = tk.Entry(self.root)
        self.log_date_entry.pack()
        tk.Label(self.root, text="Enter Hours Worked:").pack()
        self.log_hours_entry = tk.Entry(self.root)
        self.log_hours_entry.pack()
        tk.Label(self.root, text="Enter Activity Description:").pack()
        self.log_activity_entry = tk.Entry(self.root)
        self.log_activity_entry.pack()
        tk.Button(self.root, text="Log Hours", command=self.save_logged_hours).pack()

    def save_logged_hours(self):
        # Save the logged hours for the volunteer
        volunteer_id = self.log_id_entry.get()
        volunteer = self.admin.get_volunteer(volunteer_id)
        if volunteer:
            date = self.log_date_entry.get()
            hours_worked = self.log_hours_entry.get()
            activity = self.log_activity_entry.get()

            # Validate user input
            if not self.validate_not_empty(date, hours_worked, activity):
                messagebox.showerror("Error", "All fields are required!")
                return

            if not self.validate_date(date):
                messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD.")
                return

            if not self.validate_hours(hours_worked):
                messagebox.showerror("Error", "Hours worked must be a positive number!")
                return

            log = VolunteerHours(date, float(hours_worked), activity)
            volunteer.add_hours(log)
            volunteer.save_to_file()
            messagebox.showinfo("Success", "Hours logged successfully!")
        else:
            messagebox.showerror("Error", "Volunteer not found!")
        self.create_main_menu()

    def search_volunteers(self):
        # Clear the frame and show the form to search for a volunteer
        self.clear_frame()
        tk.Label(self.root, text="Enter Volunteer ID to search:").pack()
        id_entry = tk.Entry(self.root)
        id_entry.pack()
        tk.Button(self.root, text="Search", command=lambda: self.display_volunteer(id_entry.get())).pack()

    def display_volunteer(self, volunteer_id):
        # Display the volunteer information in a message box
        volunteer = self.admin.get_volunteer(volunteer_id)
        if volunteer:
            messagebox.showinfo("Volunteer Info", str(volunteer))
        else:
            messagebox.showerror("Error", "Volunteer not found!")
        self.create_main_menu()

    def generate_reports(self):
        # Clear the frame and show the form to generate reports
        self.clear_frame()
        tk.Label(self.root, text="Generate which report? (hours/summary):").pack()
        report_type_entry = tk.Entry(self.root)
        report_type_entry.pack()
        tk.Button(self.root, text="Generate", command=lambda: self.display_report(report_type_entry.get())).pack()

    def display_report(self, report_type):
        # Generate and display the selected report
        if report_type == 'hours':
            report = self.reports.generate_hours_report(self.admin)
        elif report_type == 'summary':
            report = self.reports.generate_volunteer_summary(self.admin)
        else:
            messagebox.showerror("Error", "Invalid report type!")
            return
        messagebox.showinfo("Report", report)
        self.create_main_menu()

    def exit_app(self):
        # Save all data and exit the application
        self.admin.save_all_volunteers()
        self.root.destroy()

    def volunteer_form(self, title, save_command):
        # Create a form to add or update a volunteer
        tk.Label(self.root, text=title).pack()
        tk.Label(self.root, text="ID:").pack()
        self.id_entry = tk.Entry(self.root)
        self.id_entry.pack()
        tk.Label(self.root, text="Name:").pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()
        tk.Label(self.root, text="Email:").pack()
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack()
        tk.Label(self.root, text="Contact Info:").pack()
        self.contact_entry = tk.Entry(self.root)
        self.contact_entry.pack()
        tk.Label(self.root, text="Skills (comma separated):").pack()
        self.skills_entry = tk.Entry(self.root)
        self.skills_entry.pack()
        tk.Button(self.root, text="Save", command=save_command).pack()

    def clear_frame(self):
        # Clear all widgets from the frame
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = VolunteerApp(root)
    root.mainloop()
