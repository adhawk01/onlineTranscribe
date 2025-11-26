from flask import request, jsonify
from app.services import auth_service


def register():
    data = request.json
    try:
        result = auth_service.register_user(
            email=data["user_email"],
            username=data["user_name"],
            password=data["user_password"],
            account_type=data.get("user_account_type", "user")  # optional, defaults to "user"
        )
        return jsonify(result), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": "Server error"}), 500


def login():
    data = request.json

    try:
        result = auth_service.login_user(
            email=data["user_email"],
            password=data["user_password"]
        )
        return jsonify(result), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 401
    except Exception:
        return jsonify({"error": "Server error"}), 500
