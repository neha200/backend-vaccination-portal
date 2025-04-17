import json
from flask_jwt_extended import get_jwt_identity
from functools import wraps
from flask import jsonify

def role_required(required_role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            identity = get_jwt_identity()
            try:
                # Parse the identity string into a dictionary
                identity_dict = json.loads(identity)
                if identity_dict['role'] != required_role:
                    return jsonify(msg="Access forbidden: Role mismatch"), 403
            except (json.JSONDecodeError, KeyError):
                return jsonify(msg="Invalid token structure"), 400
            return fn(*args, **kwargs)
        return wrapper
    return decorator
