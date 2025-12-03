from flask import Blueprint, jsonify
from app.controllers.home_controller import get_homepage_data

home_bp = Blueprint("home_bp", __name__)


@home_bp.route("/hello")
def hello():
    return jsonify({"message": "Hello from Flask!"})
