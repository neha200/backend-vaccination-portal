import csv
from db import mongo
from flask import Flask
from werkzeug.security import generate_password_hash
from datetime import datetime

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/vaccination_portal"
mongo.init_app(app)

def bulk_upload_users(csv_file):
    """
    Upload users from a CSV file to the database.
    """
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        users = mongo.db.users
        for row in reader:
            users.insert_one({
                "username": row["username"],
                "password_hash": generate_password_hash(row["password"]),
                "role": row["role"],  # e.g., "admin" or "user"
                "created_at": datetime.utcnow()  # Add a timestamp for user creation
            })
        print(f"Users from {csv_file} uploaded successfully.")

def bulk_upload_students(csv_file):
    """
    Upload students from a CSV file to the database.
    """
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        students = mongo.db.students
        for row in reader:
            # Handle empty or invalid date_of_vaccination
            date_of_vaccination = None
            if row["date_of_vaccination"].strip():  # Check if the field is not empty
                try:
                    date_of_vaccination = datetime.strptime(row["date_of_vaccination"], '%Y-%m-%d')
                except ValueError:
                    print(f"Invalid date format for student {row['name']}: {row['date_of_vaccination']}")
                    continue  # Skip this record if the date is invalid

            students.insert_one({
                "name": row["name"],
                "class_grade": row["class_grade"],  # e.g., "1A", "CS101"
                "student_id": row["student_id"],  # Unique 6-character ID
                "is_vaccinated": row["is_vaccinated"].lower() == "true",  # Convert to boolean
                "vaccine_name": row["vaccine_name"] if row["vaccine_name"] else None,
                "date_of_vaccination": date_of_vaccination,  # Parsed date or None
                "created_at": datetime.utcnow()  # Add a timestamp for student creation
            })
        print(f"Students from {csv_file} uploaded successfully.")

def bulk_upload_vaccination_drives(csv_file):
    """
    Upload vaccination drives from a CSV file to the database.
    """
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        drives = mongo.db.vaccination_drives
        for row in reader:
            # Handle empty or invalid date
            drive_date = None
            if row["date"].strip():  # Check if the field is not empty
                try:
                    drive_date = datetime.strptime(row["date"], '%Y-%m-%d')
                except ValueError:
                    print(f"Invalid date format for drive {row['vaccine_name']}: {row['date']}")
                    continue  # Skip this record if the date is invalid

            # Handle missing or invalid is_completed field
            is_completed = row.get("is_completed", "false").lower() == "true"

            drives.insert_one({
                "vaccine_name": row["vaccine_name"],  # Name of the vaccine
                "date": drive_date,  # Parsed date or None
                "available_doses": int(row["available_doses"]),  # Number of doses available
                "classes": row["classes"].split(",") if row["classes"] else [],  # Convert to a list of classes
                "is_completed": is_completed,  # Default to False if missing
                "created_at": datetime.utcnow()  # Add a timestamp for drive creation
            })
        print(f"Vaccination drives from {csv_file} uploaded successfully.")

with app.app_context():
    # Upload CSV files
    print("Starting data upload...")
    bulk_upload_users("users.csv")
    bulk_upload_students("students.csv")
    bulk_upload_vaccination_drives("vaccination_drives.csv")
    print("All CSV files uploaded successfully.")
