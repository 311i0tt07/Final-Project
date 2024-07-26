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

