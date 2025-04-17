from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from db import mongo
import json

auth_bp = Blueprint('auth', __name__)

# 🔐 Register a new user
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if not data.get("username") or not data.get("password") or not data.get("role"):
        return jsonify(msg="Username, password, and role are required"), 400

    # Check if user exists
    existing = mongo.db.users.find_one({"username": data["username"]})
    if existing:
        return jsonify(msg="Username already exists"), 400

    # Hash password
    hashed_pw = generate_password_hash(data["password"])
    
    # Create user
    user = {
        "username": data["username"],
        "password": hashed_pw,
        "role": data["role"]
    }

    mongo.db.users.insert_one(user)
    return jsonify(msg="User registered successfully"), 201

# 🔑 Login and get JWT
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    if not data.get("username") or not data.get("password"):
        return jsonify(msg="Username and password required"), 400

    user = mongo.db.users.find_one({"username": data["username"]})
    if not user or not check_password_hash(user["password"], data["password"]):
        return jsonify(msg="Invalid username or password"), 401

    # Generate JWT token
    token = create_access_token(identity=json.dumps({"username": user["username"], "role": user["role"]}))
    return jsonify(access_token=token), 200
