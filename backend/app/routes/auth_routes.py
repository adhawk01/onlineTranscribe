from flask import Blueprint
from app.controllers import auth_controller
from app.utils.auth_utils import token_required

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    return auth_controller.register()


@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    return auth_controller.login()


@auth_bp.route('/api/auth/protected', methods=['GET'])
@token_required
def protected_route():
    return auth_controller.protected_route()
