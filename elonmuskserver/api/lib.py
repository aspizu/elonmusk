from typing import Any

from flask import jsonify


def response_success(**kwargs: Any):
    return jsonify({"success": True, **kwargs})


def response_failure(exception: str, **kwargs: Any):
    return jsonify({"success": True, "exception": exception, **kwargs})
