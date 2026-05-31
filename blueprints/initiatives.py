from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from notifications import notify_all
import models
from extensions import socketio

initiatives_bp = Blueprint("initiatives", __name__, url_prefix="/api/initiatives")


@initiatives_bp.route("", methods=["GET"])
@login_required
def api_get_initiatives():
    initiatives = models.list_pending_initiatives(user_id=current_user.id)
    return jsonify(
        {
            "initiatives": [
                {"id": i[0], "quarter": i[1], "description": i[2]} for i in initiatives
            ]
        }
    )


@initiatives_bp.route("", methods=["POST"])
@login_required
def api_add_initiative():
    data = request.get_json() or {}
    quarter = data.get("quarter")
    description = data.get("description")
    if quarter and description:
        init_id = models.add_initiative(quarter, description, user_id=current_user.id)
        notify_all(
            subject="New Initiative Added",
            body=f"You added a new initiative for {quarter}: {description}",
            speakable_message=f"You added a new quarterly initiative for {quarter}: {description}",
        )
        socketio.emit("data_updated", {"message": "Initiative added"}, to=str(current_user.id))
        return jsonify({"message": "Initiative added.", "id": init_id}), 201
    return jsonify({"error": "Quarter and description required."}), 400


@initiatives_bp.route("/<int:initiative_id>/complete", methods=["POST"])
@login_required
def api_complete_initiative(initiative_id):
    success = models.complete_initiative(initiative_id, user_id=current_user.id)
    if success:
        notify_all(
            subject="Initiative Completed!",
            body=f"Great job completing quarterly initiative {initiative_id}.",
            speakable_message=f"Great job completing quarterly initiative {initiative_id}.",
        )
        socketio.emit("data_updated", {"message": "Initiative completed"}, to=str(current_user.id))
        return jsonify({"message": f"Initiative {initiative_id} completed."})
    return jsonify({"error": "Initiative not found."}), 404
