from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
import models
from extensions import socketio
from datetime import datetime

habits_bp = Blueprint("habits", __name__, url_prefix="/api/habits")


@habits_bp.route("", methods=["GET"])
@login_required
def api_get_habits():
    habits = models.list_habits(user_id=current_user.id)
    return jsonify({"habits": habits})


@habits_bp.route("", methods=["POST"])
@login_required
def api_add_habit():
    data = request.get_json() or {}
    description = data.get("description")
    if description:
        habit_id = models.add_habit(description, user_id=current_user.id)
        socketio.emit(
            "data_updated", {"message": "Habit added"}, to=str(current_user.id)
        )
        return jsonify({"message": "Habit added.", "id": habit_id}), 201
    return jsonify({"error": "Description required."}), 400


@habits_bp.route("/<int:habit_id>/complete", methods=["POST"])
@login_required
def api_complete_habit(habit_id):
    today = datetime.now().strftime("%Y-%m-%d")
    success = models.complete_habit(habit_id, today, user_id=current_user.id)
    if success:
        socketio.emit(
            "data_updated", {"message": "Habit completed"}, to=str(current_user.id)
        )
        return jsonify({"message": f"Habit {habit_id} completed for today."})
    return jsonify({"error": "Habit not found or already completed today."}), 400


@habits_bp.route("/<int:habit_id>", methods=["DELETE"])
@login_required
def api_delete_habit(habit_id):
    success = models.delete_habit(habit_id, user_id=current_user.id)
    if success:
        socketio.emit(
            "data_updated", {"message": "Habit deleted"}, to=str(current_user.id)
        )
        return jsonify({"message": f"Habit {habit_id} deleted."}), 200
    return jsonify({"error": "Habit not found."}), 404
