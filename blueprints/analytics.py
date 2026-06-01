from flask import Blueprint, jsonify
from flask_login import login_required, current_user
import models

analytics_bp = Blueprint("analytics", __name__)

@analytics_bp.route("/api/analytics", methods=["GET"])
@login_required
def get_analytics():
    stats = models.get_user_analytics(current_user.id)
    return jsonify(stats), 200
