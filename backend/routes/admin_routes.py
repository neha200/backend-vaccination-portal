from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import mongo
from utils.decorators import role_required
from bson.objectid import ObjectId
import csv
from io import StringIO

admin_bp = Blueprint("admin", __name__)


### Admin Dashboard
@admin_bp.route('/admin/dashboard', methods=['GET'])
@jwt_required()
@role_required('admin')
def admin_dashboard():
    return jsonify(msg="Welcome Admin!"), 200

### List All Students
@admin_bp.route('/students', methods=['GET'])
@jwt_required()
@role_required('admin')
def list_students():
    students = list(mongo.db.students.find({}, {
        "_id": 1,
        "username": 1,  # Ensure the name field is included
        "class_grade": 1,
        "student_id": 1,
        "is_vaccinated": 1,
        "vaccine_name": 1,
        "date_of_vaccination": 1
    }))
    # Convert ObjectId to string for the frontend
    for student in students:
        student["_id"] = str(student["_id"])
    return jsonify(students), 200

### Add a Student
@admin_bp.route('/students', methods=['POST'])
@jwt_required()
@role_required('admin')
def add_student():
    data = request.json
    # Validate student_id
    if not data.get("student_id"):
        return jsonify(msg="Student ID is required"), 400
    if mongo.db.students.find_one({"student_id": data["student_id"]}):
        return jsonify(msg="Student with this ID already exists"), 400
    student = {
        "username": data["username"],
        "class_grade": data["class_grade"],
        "student_id": data["student_id"],  # Ensure student_id is included
        "is_vaccinated": False
    }
    mongo.db.students.insert_one(student)
    return jsonify(msg="Student added"), 201

### Bulk Upload Students via CSV
@admin_bp.route('/students/bulk', methods=['POST'])
@jwt_required()
@role_required('admin')
def upload_csv():
    file = request.files.get('file')
    if not file:
        return jsonify(msg="No file uploaded"), 400

    stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
    reader = csv.DictReader(stream)
    added = 0
    for row in reader:
        if not row.get('username') or not row.get('class_grade') or not row.get('student_id'):
            continue
        if mongo.db.students.find_one({"student_id": row["student_id"]}):
            continue
        mongo.db.students.insert_one({
            "username": row["username"],
            "class_grade": row["class_grade"],
            "student_id": row["student_id"],  # Ensure student_id is included
            "is_vaccinated": False
        })
        added += 1
    return jsonify(msg=f"{added} students added"), 200

### Vaccinate a Student
@admin_bp.route('/students/<student_id>/vaccinate', methods=['PUT'])
@jwt_required()
@role_required('admin')
def vaccinate_student(student_id):
    data = request.json
    student = mongo.db.students.find_one({"_id": ObjectId(student_id)})
    if not student:
        return jsonify(msg="Student not found"), 404
    if student.get("is_vaccinated"):
        return jsonify(msg="Already vaccinated"), 400
    mongo.db.students.update_one(
        {"_id": ObjectId(student_id)},
        {"$set": {
            "is_vaccinated": True,
            "vaccine_name": data["vaccine_name"],
            "date_of_vaccination": data["date_of_vaccination"]
        }}
    )
    return jsonify(msg="Student vaccinated"), 200

### Update Student Details
@admin_bp.route('/students/<student_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def update_student(student_id):
    data = request.json

    # Prevent modification of student_id to null or empty
    if "student_id" in data and not data["student_id"]:
        return jsonify({"msg": "Student ID cannot be null or empty"}), 400

    # Remove `_id` from the data to prevent modification of the immutable field
    if "_id" in data:
        data.pop("_id")

    mongo.db.students.update_one({"_id": ObjectId(student_id)}, {"$set": data})
    return jsonify({"msg": "Student details updated successfully!"}), 200

### Analytics
@admin_bp.route('/analytics', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_analytics():
    try:
        # Total number of students
        total_students = mongo.db.students.count_documents({})

        # Number of vaccinated students
        vaccinated_students = mongo.db.students.count_documents({"is_vaccinated": True})

         # Fetch all drives and include the `is_completed` property
        drives = list(mongo.db.vaccination_drives.find({}, {"_id": 1, "is_completed": 1, "available_doses": 1}))
        non_completed_drives = [drive for drive in drives if not drive.get("is_completed", False)]
        
        total_drives = len(non_completed_drives)
        available_doses = sum(drive["available_doses"] for drive in non_completed_drives)

        return jsonify({
            "total_students": total_students,
            "vaccinated_students": vaccinated_students,
            "vaccination_drives": drives,
            "total_drives": total_drives,
            "available_doses": available_doses
        }), 200
    except Exception as e:
        return jsonify({"msg": f"Error fetching analytics: {str(e)}"}), 500
