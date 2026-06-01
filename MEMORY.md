# Internal Architectural Observations

## Codebase Traits
- The project is a Python application using a `click` CLI for goal tracking and a modular Flask application serving a JSON REST API.
- Vue.js 3 is used for the Single Page Application (SPA), providing frontend rendering with TypeScript and `vue-router`.
- Real-time events are managed by Flask-SocketIO. Whenever a database write happens, a `data_updated` event is emitted so that connected clients can refresh their state via the `fetchData` action in the Vue store.
- Uses Tailwind CSS v4 without a `tailwind.config.js` file.
- Components in Vue are separated into heavily modularized Single File Components under `frontend/src/components`. State is managed globally in `store.ts`.
- The Data Access Layer uses SQLAlchemy ORM, connecting to SQLite for tests/local development and PostgreSQL via Docker in production.
- Notifications are managed with Celery and Redis in `tasks.py`.

## Design Preferences
- Strict static typing in the frontend (TypeScript).
- Adopts the class strategy for Tailwind dark mode (`darkMode: 'class'`).
- Testability is key. Features must be supported with backend pytest suites and frontend E2E playwright checks.
- Changes require documentation synchronization (VISION.md, ROADMAP.md, DEPLOY.md, CHANGELOG.md, HANDOFF.md) and strict versioning rules via VERSION.md.
- Strict modularity, minimal external dependencies where possible, reactive UI without page reloads.
