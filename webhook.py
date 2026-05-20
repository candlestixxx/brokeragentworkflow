from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.twiml.voice_response import VoiceResponse
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_db_path():
    return os.getenv("DATABASE_PATH", "goals.db")

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming messages with a friendly SMS."""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    if body and body.lower().strip() == 'list':
        conn = sqlite3.connect(get_db_path())
        c = conn.cursor()
        c.execute('SELECT id, description FROM goals WHERE status = "pending"')
        goals = c.fetchall()
        conn.close()

        if not goals:
            resp.message("No pending daily goals. Great job!")
        else:
            msg = "Pending Goals:\n"
            for g in goals:
                msg += f"[{g[0]}] {g[1]}\n"
            resp.message(msg)
    else:
        # Determine the right reply for this message
        resp.message("Welcome to One-Minute Manager. Reply 'list' to see pending goals.")

    return str(resp)

@app.route("/voice", methods=['POST'])
def voice_reply():
    """Respond to incoming phone calls."""
    # Start our TwiML response
    resp = VoiceResponse()

    # Read a message aloud to the caller
    resp.say("Hello. I am your One-Minute Manager. You are doing great today. Goodbye.")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
