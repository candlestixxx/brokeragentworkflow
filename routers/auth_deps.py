from fastapi import Depends, HTTPException, Request
import os
import models

from fastapi_login import LoginManager

SECRET = os.getenv("SECRET_KEY", "super-secret-default-key-for-flashes")

manager = LoginManager(
    SECRET, token_url="/api/login", use_cookie=True, cookie_name="session"
)


@manager.user_loader()
def query_user(user_id: str):
    return models.get_user_by_id(int(user_id))


def get_current_user(user=Depends(manager)):
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user


def get_current_user_optional(request: Request):
    token = request.cookies.get("session")
    if token:
        try:
            # decode using JWT directly since manager.get_current_user is async
            import jwt

            SECRET = os.getenv("SECRET_KEY", "super-secret-default-key-for-flashes")
            payload = jwt.decode(token, SECRET, algorithms=["HS256"])
            user_id = payload.get("sub")
            if user_id:
                return query_user(user_id)
        except Exception:
            return None
    return None
