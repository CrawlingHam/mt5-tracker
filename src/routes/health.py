from src.types.responses import MT5Health, MT5Terminal
from flask import Blueprint, Response
from src.utils import to_dataclass
import MetaTrader5 as mt5

health_bp = Blueprint("health", __name__)

@health_bp.route("/health")
def health() -> Response:
    connected = mt5.initialize()

    terminal = mt5.terminal_info()._asdict() if connected else None
    
    terminal_response = to_dataclass(MT5Terminal, terminal) if terminal else None
    health_response = MT5Health(connected=connected, terminal=terminal_response)

    return health_response.jsonify()