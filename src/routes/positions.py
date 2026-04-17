from flask import Blueprint, Response, jsonify
from src.types.responses import MT5Position
from src.utils import to_dataclass
from src.routes import init_mt5
import MetaTrader5 as mt5

positions_bp = Blueprint("positions", __name__)

@positions_bp.route("/positions")
def positions() -> Response:
    init_mt5()
    
    open_positions = mt5.positions_get() or []
    position_responses = [to_dataclass(MT5Position, position._asdict()) for position in open_positions]
    return jsonify([position.to_dict() for position in position_responses])