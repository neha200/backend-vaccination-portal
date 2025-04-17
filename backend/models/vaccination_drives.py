from db import db

class VaccinationDrives(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vaccine_name = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    available_doses = db.Column(db.Integer, nullable=False)
    classes = db.Column(db.String(120))  # e.g., "5,6,7"
    is_completed = db.Column(db.Boolean, default=False)  # Boolean to track completion status

    def serialize(self):
        return {
            "id": self.id,
            "vaccine_name": self.vaccine_name,
            "date": self.date.strftime('%Y-%m-%d'),
            "available_doses": self.available_doses,
            "classes": self.classes.split(","),
            "is_completed": self.is_completed
        }
