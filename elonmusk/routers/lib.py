from typing import Any, Optional

from fastapi import Request

from ..sessions import Sessions


def success(**kwargs: Any):
    return {"success": True, "exception": None, **kwargs}


def failure(exception: str, **kwargs: Any):
    return {"success": False, "exception": exception, **kwargs}


def validate_session(req: Request) -> Optional[int]:
    token: str = req.headers["Authorization"]
    session = Sessions.get(token)
    if session:
        return session.id


def notauth():
    return failure("not_authorized")
