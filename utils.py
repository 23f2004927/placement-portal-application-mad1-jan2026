# Christiano Blairoy Fernandes
# 23f2004927
# 7 April 2026
# utils.py

from functools import wraps

from flask import redirect, session, url_for


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login"))
        else:
            return func(*args, **kwargs)

    return wrapper


def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            sessionRole = session.get("role")
            if sessionRole != role:
                return redirect(url_for("auth.login"))
            else:
                return func(*args, **kwargs)

        return wrapper

    return decorator
