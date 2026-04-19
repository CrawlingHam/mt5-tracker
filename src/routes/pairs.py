from flask import Blueprint, Response, jsonify, request
from src.types.responses import MT5PairStats, MT5PairsResponse
from src.utils import resolve_date_range
from src.types import HTTPStatusCode
from collections import Counter
from src.routes import init_mt5
import MetaTrader5 as mt5

pairs_bp = Blueprint("pairs", __name__)

@pairs_bp.route("/pairs")
def pairs() -> Response:
    init_mt5()

    from_date_raw = request.args.get("from_date")
    to_date_raw = request.args.get("to_date")

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
    symbols = [deal.symbol for deal in deals if getattr(deal, "symbol", "")]
    counts = Counter(symbols)
    total_trades = sum(counts.values())

    pair_stats = [
        MT5PairStats(
            symbol=symbol,
            trade_count=trade_count,
            trade_percentage=round((trade_count / total_trades) * 100, 2) if total_trades else 0.0,
        )
        for symbol, trade_count in counts.most_common()
    ]

    response = MT5PairsResponse(total_trades=total_trades, pairs=pair_stats)
    return response.jsonify()
