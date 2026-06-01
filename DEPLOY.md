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
- **Background Scheduler:** Run `celery -A tasks worker --loglevel=info` and `celery -A tasks beat --loglevel=info` (or via docker-compose) for background notifications and reminders instead of `scheduler.py`.

## Build Frontend (Manual)
If not using Docker: `cd frontend && npm install && npm run build` (This generates static files in `dist/`).

## Docker Production Deployment
To spin up the entire application stack including PostgreSQL, Redis, Celery beat/worker, and the Flask API serving the compiled Vue SPA:
1. Ensure Docker and Docker Compose are installed.
2. Run `docker-compose up -d --build`.
3. The app will be running and available on port `5000`.
4. Database Initialization: The application auto-initializes the database tables on first boot.
