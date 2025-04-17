from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from utils.decorators import role_required
from db import mongo
from datetime import datetime

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/analytics")

@dashboard_bp.route('/analytics', methods=['GET'])
@jwt_required()
@role_required('admin')
def dashboard_data():
    total = mongo.db.students.count_documents({})
    vaccinated = mongo.db.students.count_documents({"is_vaccinated": True})
    drives = list(mongo.db.vaccination_drives.find({
        "date": {"$gte": datetime.now().strftime("%Y-%m-%d")}
    }))
    for d in drives:
        d["_id"] = str(d["_id"])
    return jsonify({
        "total_students": total,
        "vaccinated_students": vaccinated,
        "percent_vaccinated": round((vaccinated / total) * 100, 2) if total else 0,
        "upcoming_drives": drives
    })
