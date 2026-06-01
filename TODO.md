# TODO

## Current Tasks (Phase 31: Social Accountability)
- [ ] Add `is_public` column to the `User` model in `models.py`.
- [ ] Implement `blueprints/social.py` with endpoints `/api/social/users` and `/api/social/users/<id>`.
- [ ] Implement Vue.js components (`SocialView.vue`) and update `router/index.ts`.
- [ ] Integrate into global navigation `NavBar.vue`.
- [ ] Create tests.

## Other Tasks
- [x] Phase 26: Implement Analytics Dashboard.
  - [x] Create `models.py` queries for user stats.
  - [x] Create a new Flask blueprint `analytics.py`.
  - [x] Create `AnalyticsView.vue` and add route in `router/index.ts`.
  - [x] Add link to Nav bar.
  - [x] Write Pytest and Playwright tests.
- [ ] Review UI and ensure responsiveness.
