from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from notifications import notify_all
import models
from extensions import socketio

goals_bp = Blueprint('goals', __name__, url_prefix='/api/goals')

@goals_bp.route("", methods=['GET'])
@login_required
def api_get_goals():
    goals = models.list_pending_goals(user_id=current_user.id)
    return jsonify({"goals": goals})

@goals_bp.route("", methods=['POST'])
@login_required
def api_add_goal():
    data = request.get_json() or {}
    description = data.get("description")
    parent_id = data.get("parent_id")
    if description:
        goal_id = models.add_goal(description, user_id=current_user.id, parent_id=parent_id)
        notify_all(
            subject="New Goal Added",
            body=f"You added a new goal: {description}",
            speakable_message=f"You added a new goal: {description}"
        )
        socketio.emit('data_updated', {"message": "Goal added"})
        return jsonify({"message": "Goal added.", "id": goal_id}), 201
    return jsonify({"error": "Description required."}), 400

@goals_bp.route("/<int:goal_id>/complete", methods=['POST'])
@login_required
def api_complete_goal(goal_id):
    success = models.complete_goal(goal_id, user_id=current_user.id)
    if success:
        notify_all(
            subject="Goal Completed!",
            body=f"Excellent work! You completed goal {goal_id}.",
            speakable_message=f"Excellent work! You completed goal {goal_id}."
        )
        socketio.emit('data_updated', {"message": "Goal completed"})
        return jsonify({"message": f"Goal {goal_id} completed."})
    return jsonify({"error": "Goal not found."}), 404
