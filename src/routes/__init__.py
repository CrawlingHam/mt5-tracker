import MetaTrader5 as mt5
from flask import Flask

def init_mt5() -> None:
    if not mt5.initialize():
        raise RuntimeError(f"MT5 init failed: {mt5.last_error()}")


def register_routes(app: Flask) -> None:
    from .positions import positions_bp
    from .account import account_bp
    from .health import health_bp
    from .trades import trades_bp
    from .pairs import pairs_bp
    from .all import all_bp

    app.register_blueprint(positions_bp)
    app.register_blueprint(account_bp)
    app.register_blueprint(trades_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(pairs_bp)
    app.register_blueprint(all_bp)