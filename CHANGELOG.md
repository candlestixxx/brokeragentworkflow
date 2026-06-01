# Changelog
## [0.25.0] - User Notification Settings Toggle
- Formatted `models.py` tracking Boolean default values managing active system settings directly across user schema interactions seamlessly.
- Bound `POST /api/me/settings` natively processing variables securely.
- Expanded Celery worker functions inside `tasks.py` to pre-emptively query user settings terminating job prompts immediately if users individually opt-out organically.
- Re-architected `App.vue` providing a new `/settings` Router layout utilizing native `HeadlessUI` Toggle `Switch` elements directly.

## [0.24.0] - Tailwind Global Dark Mode
- Updated `tailwind.config.js` tracking dynamic UI `darkMode` capabilities via native HTML5 bindings structurally explicitly targeting `class` structures natively toggling `document.documentElement` behaviors dynamically.
- Intercepted HeroIcons SVG interactions integrating dual-action `MoonIcon` and `SunIcon` models explicitly bound to the Vue 3 header component layout efficiently tracking CSS logic cleanly gracefully triggering `.dark:*` overlays inherently.

## [0.23.0] - Continuous Integration & Ruff Code Quality Standardization
- Established `.github/workflows/ci.yml` initializing GitHub Actions mapping continuous integration tests natively covering Pytest workflows and Vite compilations recursively.
- Re-architected backend structures parsing formats utilizing `ruff` explicitly standardizing Python syntactic integrity preventing regressions logically.

## [0.22.0] - Accessible Headless UI Component Replacements
- Decoupled manual `v-if` toggle behaviors bounding tab/modal logic securely introducing `@headlessui/vue` elements natively capturing proper ARIA DOM rendering.
- Embedded `@heroicons/vue` integrating visually consistent SVG elements cleanly directly inside Vue execution templates bypassing arbitrary external CSS library queries.

## [0.21.0] - Frontend Vue-Router Navigation
- Installed `vue-router@4` introducing exact URL history manipulation directly bypassing implicit DOM reactiveness states.
- Bound `/login`, `/register`, and `/` explicitly into targeted `DashboardView`, `LoginView`, and `RegisterView` components wrapping conditional navigation layers.
- Validated Chromium traversal algorithms tracking router execution paths sequentially via Playwright E2E frameworks.

## [0.20.0] - TypeScript Frontend Migration
- Established strict TypeScript configuration environments leveraging `tsconfig.json` & `vue-tsc`.
- Migrated all `frontend/src/*` logic mapping `main.js` and `store.js` over to strict `*.ts` extensions mapping explicit interfaces for User, Goal, and Initiative schemas.
- Modified Vue components into `<script setup lang="ts">` binding variables eliminating unmapped runtime exceptions.

## [0.19.0] - Frontend Vue Component Modularization
- Re-architected monolithic `App.vue` entrypoint down into targeted Single File Components (`NavBar.vue`, `AuthTabs.vue`, `ActiveGoals.vue`, `CompletedGoals.vue`, `CalendarGoals.vue`, `QuarterlyInitiatives.vue`).
- Abstracted reactive context parameters handling global application tracking into a centralized `store.js` state.

## [0.18.0] - Chronological Calendar View
- Added a `models.list_calendar_goals` data-layer query fetching all goals grouped by their `created_at` timestamp array.
- Mounted `GET /api/goals/calendar` to map timeline logic outwards to the frontend.
- Augmented the `App.vue` UI with a `Calendar` tab rendering visual history of historical objectives partitioned strictly by distinct operational days.

## [0.17.0] - User Avatars
- Added an `avatar_url` database column to the `User` model.
- Established `POST /api/me/avatar` to securely bind profile URLs to authenticated users.
- Updated the Vue front-end navigation header implementing default user-initial placeholders parsing from `ui-avatars.com` alongside a clean visual hover-modal UI allowing end-users to customize profile pictures seamlessly.

## [0.16.0] - Completed Goals History
- Developed a new `list_completed_goals()` data-layer query fetching goals marked `status == 'completed'`.
- Added the `/api/goals/completed` endpoint to expose goal history payload.
- Refactored `App.vue` introducing a dual-tab "Active" vs "History" selector, empowering users to review accomplished objectives visually.

## [0.15.0] - Hierarchical Sub-Goals
- Enhanced the Data Model by adding a self-referential `parent_id` to the `Goal` entity.
- Expanded the `/api/goals` GET payload to serialize and nest sub-goals intrinsically.
- Added UI inline forms to parent goals on the dashboard allowing "+ Sub-goal" creation and individual completion tracking.

## [0.14.0] - Vite and Vue 3 Frontend Migration
- Deprecated monolithic `spa.html` CDN approach.
- Implemented a structured Node.js frontend pipeline utilizing Vite, Vue 3 Single File Components (SFCs), and TailwindCSS PostCSS bindings.
- Updated `docker-compose.yml` and `Dockerfile` to handle multi-stage builds (`npm run build` translating to `/dist`).
- Re-routed Flask Blueprint `views.py` to seamlessly serve generated `dist/` static files.

## [0.13.0] - Playwright End-to-End Testing
- Integrated `playwright` and `pytest-playwright` into the testing framework.
- Developed a comprehensive `test_e2e.py` suite mimicking actual user browser behavior for multi-tenant Registration, Login, and Goal Tracking loops.

## [0.12.0] - Celery and Redis Task Queue
- Migrated background daemon methodology from `APScheduler` to a robust `celery` + `redis` worker infrastructure.
- Replaced `scheduler.py` with `tasks.py` to handle `@celery_app.task` dispatching for daily and weekly prompts.
- Updated `docker-compose.yml` to orchestrate `redis`, `celery_worker`, and `celery_beat` services simultaneously alongside the Flask API.

## [0.11.0] - Architecture Scaling with Flask Blueprints
- Refactored monolithic `app.py` architecture into modular Flask Blueprints.
- Extracted routing into `/blueprints/views.py`, `auth.py`, `goals.py`, `initiatives.py`, and `webhooks.py`.
- Improved codebase maintainability while preserving API contracts and WebSocket integrations.

## [0.10.0] - Real-Time WebSockets
- Integrated `Flask-SocketIO` to push real-time updates directly to the Vue frontend when backend database modifications occur, keeping multiple browser sessions perfectly synced.

## [0.9.0] - Vue.js Single Page Application
- Refactored `app.py` from server-side rendering to a JSON REST API.
- Created `spa.html` implementing a Vue 3 reactive interface for seamless state updates without page reloading.
- Removed legacy Jinja templates.

## [0.8.0] - User Authentication
- Added `Flask-Login` and `Flask-Bcrypt` to support multi-tenant user authentication.
- Added `User` data model and linked goals and initiatives via `user_id` foreign keys.
- Implemented `/login`, `/register`, and `/logout` routes in the Web Dashboard.

## [0.7.0] - PostgreSQL Integration
- Added `psycopg2-binary` to support PostgreSQL.
- Updated `docker-compose.yml` to orchestrate a dedicated `db` container running `postgres:15-alpine`.
- Refactored `models.py` logic to seamlessly toggle between PostgreSQL (production) and local SQLite (testing/local CLI).

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

## 0.26.0
- **Feature**: Implemented Phase 26 Analytics Dashboard.
  - Added new `/api/analytics` backend endpoint using `blueprints/analytics.py` and `models.get_user_analytics()`.
  - Added frontend `AnalyticsView.vue` with responsive charts tracking Total Goals, Completed Goals, Completion Rate, and Day Streak.
  - Updated Vue Router and NavBar to support the new Analytics route.
  - Tested logic extensively via `test_analytics.py` and E2E `test_playwright_analytics.py`.
