from db import db

class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    class_grade = db.Column(db.String(10), nullable=False)
    student_id = db.Column(db.string(50), unique=True, nullable=False)
    is_vaccinated = db.Column(db.Boolean, default=False)
    vaccine_name = db.Column(db.String(120), nullable=True)
    date_of_vaccination = db.Column(db.DateTime, nullable=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "class_grade": self.class_grade,
            "student_id": self.student_id,
            "is_vaccinated": self.is_vaccinated,
            "vaccine_name": self.vaccine_name,
            "date_of_vaccination": self.date_of_vaccination.strftime('%Y-%m-%d') if self.date_of_vaccination else None
        }
