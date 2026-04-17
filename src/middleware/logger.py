from flask import Flask, g, request
import logging
import time

_request_logger = logging.getLogger("src.request")

def setup_request_logger(app: Flask) -> None:
    if not _request_logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        _request_logger.addHandler(handler)
    _request_logger.setLevel(logging.INFO)
    _request_logger.propagate = False

    @app.before_request
    def _log_request_start() -> None:
        g.request_start_time = time.perf_counter()

    @app.after_request
    def _log_request_end(response):
        duration_ms = (time.perf_counter() - g.request_start_time) * 1000
        _request_logger.info(
            "%s %s -> %s (%.2f ms)",
            request.method,
            request.path,
            response.status_code,
            duration_ms,
        )
        return response
