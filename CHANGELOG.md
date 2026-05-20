# Changelog
## [0.6.0] - Tailwind CSS UI Overhaul
- Upgraded the raw HTML/CSS web dashboard to a modern, responsive design using Tailwind CSS.

## [0.5.0] - ORM Migration and Dockerization
- Migrated the raw SQLite data access layer in `models.py` to use SQLAlchemy ORM, improving safety and maintainability.
- Containerized the application using a `Dockerfile` and `docker-compose.yml` that orchestrates the web server and background scheduler independently.

## [0.4.0] - Web Dashboard
- Expanded `webhook.py` into `app.py` functioning as a full Flask web server.
- Added `templates/layout.html` and `templates/dashboard.html`.
- Implemented a graphical user interface for visualizing, adding, and completing daily goals and quarterly initiatives.

## [0.3.0] - Database Refactor and Scheduled Triggers
- Refactored all direct SQLite database execution out of the CLI/Webhook layer and into a dedicated `models.py` module.
- Added `scheduler.py` using APScheduler to trigger daily and weekly reminders via Twilio and SMTP.

## [0.2.0] - Quarterly Planning and Webhooks
- Added new table `quarterly_initiatives` to track larger quarterly initiatives.
- Added `add-initiative`, `list-initiatives`, and `complete-initiative` to the CLI.
- Added a Twilio webhook (`webhook.py`) via Flask to handle incoming SMS/Voice messages dynamically.

## [0.1.0] - Core Implementation
- Bootstrapped project layout.
- Added `cli.py` for tracking daily "One-Minute Goals" via `add`, `list`, and `complete`.
- Added programmable notifications for email and text/voice (via Twilio).

## [0.0.0] - Initial Setup
- Initialized core project documentation.
