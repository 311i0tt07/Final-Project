import sqlite3
import os
from volunteer import Volunteer
from volunteer_hours import VolunteerHours

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
