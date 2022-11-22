from typing import Any


def success(**kwargs: Any):
    return {"success": True, **kwargs}


def failure(exception: str, **kwargs: Any):
    return {"success": False, "exception": exception, **kwargs}
