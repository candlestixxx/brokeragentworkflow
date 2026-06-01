# Deployment Instructions
1. **Prerequisites:** Docker, Docker-Compose.
2. **Environment Variables:** Copy `.env.example` to `.env` and fill in `SECRET_KEY`, `DATABASE_URL` (optional, defaults to SQLite), `REDIS_URL`, etc.
3. **Build Frontend:** `cd frontend && npm install && npm run build` (This generates static files in `dist/`).
4. **Run Backend (Docker):** `docker-compose up -d --build` (This spins up the web server, Celery worker, and Redis).
5. **Database Initialization:** The application auto-initializes the database tables on first boot.
