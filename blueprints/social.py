from flask import Blueprint, jsonify
from flask_login import login_required
import models

social_bp = Blueprint('social', __name__, url_prefix='/api/social')

@social_bp.route('/users', methods=['GET'])
@login_required
def get_public_users():
    users = models.list_public_users()
    return jsonify(users)

@social_bp.route('/users/<int:user_id>/profile', methods=['GET'])
@login_required
def get_user_profile(user_id):
    user = models.get_user_by_id(user_id)
    if not user or not user.is_public:
        return jsonify({"error": "User not found or is private"}), 404

    recent_completed = models.list_completed_goals(user_id=user.id)
    # limit to 10
    recent_completed = recent_completed[:10]

    return jsonify({
        "id": user.id,
        "username": user.username,
        "avatar_url": user.avatar_url,
        "recent_completed_goals": recent_completed
    })
