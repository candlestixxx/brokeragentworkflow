from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
import models

auth_bp = Blueprint('auth', __name__, url_prefix='/api')

@auth_bp.route("/me", methods=['GET'])
def api_me():
    if current_user.is_authenticated:
        return jsonify({
            "authenticated": True,
            "username": current_user.username,
            "avatar_url": current_user.avatar_url
        })
    return jsonify({"authenticated": False})

@auth_bp.route("/me/avatar", methods=['POST'])
@login_required
def api_update_avatar():
    data = request.get_json() or {}
    avatar_url = data.get('avatar_url')
    if not avatar_url:
        return jsonify({"error": "Avatar URL required."}), 400

    success = models.update_user_avatar(current_user.id, avatar_url)
    if success:
        return jsonify({"message": "Avatar updated."})
    return jsonify({"error": "Update failed."}), 500

@auth_bp.route("/login", methods=['POST'])
def api_login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    user = models.get_user_by_username(username)
    if user and user.check_password(password):
        login_user(user)
        return jsonify({"message": "Logged in successfully."})
    return jsonify({"error": "Invalid username or password."}), 401

@auth_bp.route("/register", methods=['POST'])
def api_register():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "Username and password required."}), 400
    if models.get_user_by_username(username):
        return jsonify({"error": "Username already exists."}), 409

    user_id = models.create_user(username, password)
    if user_id:
        return jsonify({"message": "Registration successful."}), 201
    return jsonify({"error": "Registration failed."}), 500

@auth_bp.route("/logout", methods=['POST'])
@login_required
def api_logout():
    logout_user()
    return jsonify({"message": "Logged out successfully."})
