import os
import smtplib
from email.message import EmailMessage

def is_notifications_enabled():
    return os.getenv("NOTIFICATIONS_ENABLED", "false").lower() == "true"

def send_email(subject, body):
    if not is_notifications_enabled():
        return False

    host = os.getenv("SMTP_HOST")
    port = int(os.getenv("SMTP_PORT", "587"))
    user = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASS")
    from_email = os.getenv("EMAIL_FROM")
    to_email = os.getenv("EMAIL_TO")

    if not all([host, user, password, from_email, to_email]):
        print("Warning: Email notifications enabled but missing SMTP config.")
        return False

    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email

        server = smtplib.SMTP(host, port)
        server.starttls()
        server.login(user, password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

def send_sms(body):
    if not is_notifications_enabled():
        return False

    sid = os.getenv("TWILIO_ACCOUNT_SID")
    token = os.getenv("TWILIO_AUTH_TOKEN")
    from_num = os.getenv("TWILIO_FROM_NUMBER")
    to_num = os.getenv("TWILIO_TO_NUMBER")

    if not all([sid, token, from_num, to_num]):
        print("Warning: SMS notifications enabled but missing Twilio config.")
        return False

    try:
        from twilio.rest import Client
        client = Client(sid, token)
        client.messages.create(body=body, from_=from_num, to=to_num)
        return True
    except ImportError:
        print("Warning: twilio package not installed. Cannot send SMS.")
        return False
    except Exception as e:
        print(f"Failed to send SMS: {e}")
        return False

def make_call(message):
    if not is_notifications_enabled():
        return False

    sid = os.getenv("TWILIO_ACCOUNT_SID")
    token = os.getenv("TWILIO_AUTH_TOKEN")
    from_num = os.getenv("TWILIO_FROM_NUMBER")
    to_num = os.getenv("TWILIO_TO_NUMBER")

    if not all([sid, token, from_num, to_num]):
        print("Warning: Call notifications enabled but missing Twilio config.")
        return False

    try:
        from twilio.rest import Client
        import html
        client = Client(sid, token)
        # Using Twilio's TwiML bin to speak the message
        escaped_message = html.escape(message)
        twiml = f'<Response><Say>{escaped_message}</Say></Response>'
        client.calls.create(twiml=twiml, from_=from_num, to=to_num)
        return True
    except ImportError:
        print("Warning: twilio package not installed. Cannot make call.")
        return False
    except Exception as e:
        print(f"Failed to make call: {e}")
        return False

def notify_all(subject, body, speakable_message):
    send_email(subject, body)
    send_sms(body)
    make_call(speakable_message)
