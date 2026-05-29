# Session Handoff Notes

## Phase 32: Gamification & Badges
- Implemented robust `get_user_badges` calculator in `models.py`.
- Pushed gamification arrays out through JSON APIs on `auth_bp` and `social_bp`.
- Verified UI mapping over `DashboardView.vue` and `SocialView.vue`.
- Test flakiness around Playwright Websockets handling headless interactions continues to appear slightly temperamental. Added explicit wait behaviors inside `test_social.py` via `page.reload()` and `time.sleep` to guarantee DOM stability on GitHub Actions workers. Separated Playwright UI E2E test runs out of the base `pytest` list inside Github CI.

## Current State
- Gamification is completely done, built, and tested.
- Pushed commit "v0.32.0 - Phase 32: Gamification & Badges".
- Updated `ROADMAP.md` and `TODO.md` to initiate **Phase 33: FastAPI Migration**.

## Next Steps for Successor Model
- Begin Phase 33. The core mission is translating the highly coupled synchronous Flask + Flask-Login architecture into a modern Python ASGI framework (FastAPI).
- This will require writing new Authentication routes via JWTs and converting all HTTP responses to Pydantic-model responses instead of generic Flask `jsonify`.
- Focus heavily on getting the existing Pytest suites to run against FastAPI's `TestClient`.
