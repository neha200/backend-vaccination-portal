from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from utils.decorators import role_required
from db import mongo
from datetime import datetime, timedelta
from bson.objectid import ObjectId
from bson.errors import InvalidId

drive_bp = Blueprint("drive", __name__, url_prefix="/drives")

@drive_bp.route('', methods=['POST'])
@jwt_required()
@role_required('admin')
def create_drive():
    data = request.json

    # Validate required fields
    if not data.get("vaccine_name") or not data.get("date") or not data.get("available_doses") or not data.get("classes"):
        return jsonify(msg="All fields are required"), 400

    try:
        date_obj = datetime.strptime(data["date"], "%Y-%m-%d")
        current_date = datetime.now()

        # Validation: If the drive date is in the future, ensure it is more than 15 days ahead
        if date_obj > current_date:
            date_difference = (date_obj - current_date).days
            if date_difference <= 15:
                return jsonify(msg="Drive must be at least 15 days ahead"), 400

        # Validation: If the drive date is in the past, ensure "is_completed" is True
        if date_obj < current_date and not data.get("is_completed", False):
            return jsonify(msg="For past dates, the drive must be marked as completed"), 400

        # Prepare the drive data for insertion
        drive = {
            "vaccine_name": data["vaccine_name"],
            "date": data["date"],
            "available_doses": int(data["available_doses"]),
            "classes": data["classes"].split(","),  # Convert comma-separated string to list
            "is_completed": data.get("is_completed", False)  # Default to False if not provided
        }

        # Insert the drive into the database
        mongo.db.vaccination_drives.insert_one(drive)
        return jsonify(msg="Drive created successfully"), 201

    except ValueError:
        return jsonify(msg="Invalid date format. Use YYYY-MM-DD"), 400

@drive_bp.route('/', methods=['GET'])
@jwt_required()
def list_drives():
    drives = list(mongo.db.vaccination_drives.find({}))
    for d in drives:
        d["_id"] = str(d["_id"])  # Convert ObjectId to string
    return jsonify(drives)

@drive_bp.route('/<id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def update_drive(id):
    data = request.json
    mongo.db.vaccination_drives.update_one(
        {"_id": ObjectId(id)},
        {"$set": {
            "vaccine_name": data["vaccine_name"],
            "date": data["date"],
            "available_doses": int(data["available_doses"]),
            "classes": data["classes"].split(",")  # Convert comma-separated string to list
        }}
    )
    return jsonify(msg="Drive updated successfully"), 200

@drive_bp.route('/<id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_drive(id):
    try:
        # Validate the ObjectId
        object_id = ObjectId(id)
    except InvalidId:
        return jsonify(msg="Invalid drive ID"), 400

    # Attempt to delete the drive
    result = mongo.db.vaccination_drives.delete_one({"_id": object_id})
    if result.deleted_count == 0:
        return jsonify(msg="Drive not found"), 404
    return jsonify(msg="Drive deleted successfully"), 200

@drive_bp.route('/student/<student_id>', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_drive_for_student(student_id):
    drive = mongo.db.vaccination_drives.find_one({"registered_students": student_id})
    if not drive:
        return jsonify(msg="No vaccination drive found for this student"), 404
    return jsonify({
        "vaccine_name": drive["vaccine_name"]
    }), 200

@drive_bp.route('/vaccination_drives', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_vaccination_drives():
    drives = mongo.db.vaccination_drives.find()
    drives_list = []
    for drive in drives:
        drives_list.append({
            "_id": str(drive["_id"]),
            "vaccine_name": drive["vaccine_name"],
            "date": drive["date"],
            "is_completed": drive.get("is_completed", False)  # Default to False if missing
        })
    return jsonify(drives_list), 200
