from flask import Blueprint, Response, jsonify, request
from src.utils import  to_dataclass, resolve_date_range
from src.dto import aggregate_trades_by_position
from src.types.responses import MT5Trade
from src.types import HTTPStatusCode
from src.routes import init_mt5
from dataclasses import asdict
import MetaTrader5 as mt5

trades_bp = Blueprint("trades", __name__)

@trades_bp.route("/trades")
def trades() -> Response:
    init_mt5()

    from_date_raw = request.args.get("from_date")
    to_date_raw = request.args.get("to_date")
    dto_raw = request.args.get("dto")
    use_dto = dto_raw is not None and dto_raw.lower() in ("1", "true", "yes", "on")

    try:
        from_date, to_date = resolve_date_range(from_date_raw, to_date_raw)
    except ValueError:
        return (
            jsonify({"error": "Invalid date format. Use ISO format, e.g. 2025-01-01 or 2025-01-01T13:45:00"}),
            HTTPStatusCode.BAD_REQUEST,
        )

    if from_date > to_date:
        return jsonify({"error": "from_date cannot be greater than to_date"}), HTTPStatusCode.BAD_REQUEST

    deals = mt5.history_deals_get(from_date, to_date) or []
    trade_responses = [to_dataclass(MT5Trade, deal._asdict()) for deal in deals]
    if use_dto:
        return jsonify([asdict(row) for row in aggregate_trades_by_position(trade_responses)])
    return jsonify([asdict(trade) for trade in trade_responses])