from src.types.responses import MT5Account, MT5AllResponse, MT5Health, MT5Position, MT5Terminal, MT5Trade
from flask import Blueprint, Response, jsonify, request
from src.utils import to_dataclass, resolve_date_range
from src.dto import aggregate_trades_by_position
from src.types import HTTPStatusCode
from src.routes import init_mt5
import MetaTrader5 as mt5

all_bp = Blueprint("all", __name__)

@all_bp.route("/all")
def all_data() -> Response:
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
    open_positions = mt5.positions_get() or []
    account_info = mt5.account_info()
    terminal = mt5.terminal_info()

    position_responses = [to_dataclass(MT5Position, position._asdict()) for position in open_positions]
    account_response = to_dataclass(MT5Account, account_info._asdict()) if account_info else None
    terminal_response = to_dataclass(MT5Terminal, terminal._asdict()) if terminal else None
    trade_responses = [to_dataclass(MT5Trade, deal._asdict()) for deal in deals]
    trades_payload = aggregate_trades_by_position(trade_responses) if use_dto else trade_responses
    health_response = MT5Health(connected=True, terminal=terminal_response)

    all_response = MT5AllResponse(
        positions=position_responses,
        account=account_response,
        trades=trades_payload,
        health=health_response,
    )

    return all_response.jsonify()