from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse
import models

webhooks_bp = Blueprint("webhooks", __name__)


@webhooks_bp.route("/sms", methods=["POST"])
def sms_reply():
    """Respond to incoming messages with a friendly SMS."""
    # Get the message the user sent our Twilio number
    body = request.values.get("Body", None)

    # Start our TwiML response
    resp = MessagingResponse()

    if body and body.lower().strip() == "list":
        # Defaulting to user_id=1 for now as per previous constraints
        goals = models.list_pending_goals(user_id=1)

        if not goals:
            resp.message("No pending daily goals. Great job!")
        else:
            msg = "Pending Goals:\n"
            for g in goals:
                msg += f"[{g['id']}] {g['description']}\n"
                for sub in g.get("subgoals", []):
                    msg += f"    - [{sub['id']}] {sub['description']}\n"
            resp.message(msg)
    else:
        # Determine the right reply for this message
        resp.message(
            "Welcome to One-Minute Manager. Reply 'list' to see pending goals."
        )

    return str(resp)


@webhooks_bp.route("/voice", methods=["POST"])
def voice_reply():
    """Respond to incoming phone calls."""
    # Start our TwiML response
    resp = VoiceResponse()

    # Read a message aloud to the caller
    resp.say("Hello. I am your One-Minute Manager. You are doing great today. Goodbye.")

    return str(resp)
