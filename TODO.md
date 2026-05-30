# TODO
1. Execute Phase 33: Migrate Flask to FastAPI.

## Immediate Tasks (Phase 33)
- [ ] Create `main.py` entrypoint for FastAPI, replacing `app.py`.
- [ ] Rewrite REST API blueprints into FastAPI routers (auth, goals, habits, social).
- [ ] Replace Flask-Login with JWT/OAuth2 mechanisms for frontend authentication.
- [ ] Refactor WebSockets (Flask-SocketIO) to native FastAPI WebSockets.
- [ ] Update frontend Vue store/API calls to handle JWT authentication.