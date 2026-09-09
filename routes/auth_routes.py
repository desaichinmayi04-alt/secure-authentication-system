from flask import Blueprint, request, jsonify
from src.auth import AuthenticationSystem

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
auth_system = AuthenticationSystem()


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'status': 'error', 'message': 'Username and password required'}), 400

    success, message = auth_system.register(username, password)

    if success:
        return jsonify({'status': 'success', 'message': message}), 201
    else:
        return jsonify({'status': 'error', 'message': message}), 400


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'status': 'error', 'message': 'Username and password required'}), 400

    success, message = auth_system.login(username, password)

    if success:
        return jsonify({'status': 'success', 'message': message}), 200
    else:
        return jsonify({'status': 'error', 'message': message}), 401
