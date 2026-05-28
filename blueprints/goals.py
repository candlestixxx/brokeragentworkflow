from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from notifications import notify_all
import models
from extensions import socketio

goals_bp = Blueprint("goals", __name__, url_prefix="/api/goals")


@goals_bp.route("", methods=["GET"])
@login_required
def api_get_goals():
    goals = models.list_pending_goals(user_id=current_user.id)
    return jsonify({"goals": goals})


@goals_bp.route("/completed", methods=["GET"])
@login_required
def api_get_completed_goals():
    goals = models.list_completed_goals(user_id=current_user.id)
    return jsonify({"goals": goals})


@goals_bp.route("/calendar", methods=["GET"])
@login_required
def api_get_calendar_goals():
    calendar_data = models.list_calendar_goals(user_id=current_user.id)
    return jsonify({"calendar": calendar_data})


@goals_bp.route("", methods=["POST"])
@login_required
def api_add_goal():
    data = request.get_json() or {}
    description = data.get("description")
    parent_id = data.get("parent_id")
    if description:
        goal_data = models.add_goal(
            description, user_id=current_user.id, parent_id=parent_id
        )
        notify_all(
            subject="New Goal Added",
            body=f"You added a new goal: {description}",
            speakable_message=f"You added a new goal: {description}",
        )
        socketio.emit("goal_added", {"goal": goal_data}, to=str(current_user.id))
        return jsonify({"message": "Goal added.", "id": goal_data["id"]}), 201
    return jsonify({"error": "Description required."}), 400


@goals_bp.route("/<int:goal_id>/complete", methods=["POST"])
@login_required
def api_complete_goal(goal_id):
    success = models.complete_goal(goal_id, user_id=current_user.id)
    if success:
        notify_all(
            subject="Goal Completed!",
            body=f"Excellent work! You completed goal {goal_id}.",
            speakable_message=f"Excellent work! You completed goal {goal_id}.",
        )
        socketio.emit("goal_completed", {"id": goal_id}, to=str(current_user.id))
        return jsonify({"message": f"Goal {goal_id} completed."})
    return jsonify({"error": "Goal not found."}), 404


@goals_bp.route("/<int:goal_id>", methods=["DELETE"])
@login_required
def api_delete_goal(goal_id):
    success = models.delete_goal(goal_id, user_id=current_user.id)
    if success:
        socketio.emit("goal_deleted", {"id": goal_id}, to=str(current_user.id))
        return jsonify({"message": f"Goal {goal_id} deleted."}), 200
    return jsonify({"error": "Goal not found."}), 404


@goals_bp.route("/breakdown", methods=["POST"])
@login_required
def api_breakdown_goal():
    """
    Simulates an AI service parsing a high-level goal description
    and returning a list of granular one-minute sub-goals.
    """
    data = request.get_json() or {}
    description = data.get("description", "")

    if not description:
        return jsonify({"error": "Description required."}), 400

    # Simulate an AI response by echoing back string splits or generic chunks
    sub_goals = [
        f"Research best approaches for: {description[:20]}...",
        f"Draft initial outline for: {description[:20]}...",
        f"Execute and review first steps of: {description[:20]}...",
    ]

    return jsonify({"subgoals": sub_goals}), 200
