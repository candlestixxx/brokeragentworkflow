# TODO

## Current Tasks (Phase 33: Next Features)
- [ ] TBD.

## Completed Tasks
- [x] Phase 32: FastAPI Backend Migration.
  - [x] Initialize FastAPI application in `main.py`.
  - [x] Port `auth.py` logic to FastAPI dependencies.
  - [x] Port `goals.py` and `habits.py` endpoints.
  - [x] Port `social.py` and `analytics.py` endpoints.
  - [x] Update frontend to point to FastAPI backend (if port changes).
- [x] Phase 31: Social Accountability.
  - [x] Add `is_public` column to the `User` model in `models.py`.
  - [x] Implement `blueprints/social.py` with endpoints `/api/social/users` and `/api/social/users/<id>`.
  - [x] Implement Vue.js components (`SocialView.vue`) and update `router/index.ts`.
  - [x] Integrate into global navigation `NavBar.vue`.
  - [x] Create tests.
- [x] Phase 26: Implement Analytics Dashboard.
