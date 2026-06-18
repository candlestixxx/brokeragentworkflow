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
        socketio.emit("goal_added", {"goal": {"id": goal_data, "description": description, "parent_id": parent_id}}, to=str(current_user.id))
        return jsonify({"message": "Goal added.", "id": goal_data}), 201
    return jsonify({"error": "Description required."}), 400


@goals_bp.route("/<int:goal_id>/complete", methods=["POST"])
@login_required
def api_complete_goal(goal_id):
    success = models.complete_goal(goal_id, user_id=current_user.id)
    if success:
        # Evaluate badges after completion
        new_badges = models.evaluate_badges(current_user.id)

        notify_all(
            subject="Goal Completed!",
            body=f"Excellent work! You completed goal {goal_id}.",
            speakable_message=f"Excellent work! You completed goal {goal_id}.",
        )

        # Emit goal completed event
        socketio.emit("goal_completed", {"id": goal_id}, to=str(current_user.id))
        
        # Emit data updated event for general UI refresh
        socketio.emit("data_updated", {"message": "Goal completed"}, to=str(current_user.id))

        # If new badges were awarded, notify the user
        for badge in new_badges:
            socketio.emit("badge_awarded", {"name": badge["name"], "icon": badge["icon"]}, to=str(current_user.id))

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


@goals_bp.route("/<int:goal_id>/breakdown", methods=["POST"])
@login_required
def api_breakdown_goal(goal_id):
    """
    Simulates an AI service parsing a high-level goal description
    and returning a list of granular one-minute sub-goals.
    """
    goal = models.get_user_by_id(current_user.id).goals
    # Find the specific goal
    target_goal = None
    for g in goal:
        if g.id == goal_id:
            target_goal = g
            break
    
    if not target_goal:
        return jsonify({"error": "Goal not found."}), 404

    description = target_goal.description

    # Simulate an AI response by echoing back string splits or generic chunks
    sub_goals = [
        f"Research best approaches for: {description[:20]}...",
        f"Draft initial outline for: {description[:20]}...",
        f"Execute and review first steps of: {description[:20]}..."
    ]

    # Automatically add them as subgoals
    for sub_desc in sub_goals:
        models.add_goal(sub_desc, user_id=current_user.id, parent_id=goal_id)

    return jsonify({"subgoals": sub_goals}), 200


@goals_bp.route("/breakdown", methods=["POST"])
@login_required
def api_breakdown_goal_legacy():
    """Legacy endpoint for tests or other callers."""
    data = request.get_json() or {}
    description = data.get("description", "")

    if not description:
        return jsonify({"error": "Description required."}), 400

    sub_goals = [
        f"Research best approaches for: {description[:20]}...",
        f"Draft initial outline for: {description[:20]}...",
        f"Execute and review first steps of: {description[:20]}..."
    ]

    return jsonify({"subgoals": sub_goals}), 200
