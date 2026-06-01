# Deployment Instructions
The project contains a CLI, a web dashboard, and an automated background scheduler.

## Local Setup
1. Clone the repository.
2. Ensure you have Python 3.10+ installed.
3. Create a virtual environment: `python3 -m venv venv && source venv/bin/activate`
4. Run `pip install -r requirements.txt`.
5. Copy `.env.example` to `.env` and configure your API keys (Twilio/SMTP) if desired.

## Running the Application
- **Web Dashboard & Webhooks:** Run `flask run` (or `python app.py` if configured) to start the web UI on `http://127.0.0.1:5000`.
- **Command Line Interface:** Run `python cli.py --help` to see CLI commands.
- **Background Scheduler:** Run `python scheduler.py` in a separate terminal to start the background daemon that handles automated prompts and reminders.
