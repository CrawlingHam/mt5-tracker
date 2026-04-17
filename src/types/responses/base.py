from flask import Response, jsonify
from dataclasses import asdict

__all__ = ["ResponseModel"]

class ResponseModel:
    def to_dict(self) -> dict:
        return asdict(self)

    def jsonify(self) -> Response:
        return jsonify(self.to_dict())
