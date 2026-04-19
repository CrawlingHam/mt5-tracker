from __future__ import annotations
from src.types.responses.trade import MT5Trade, MT5PositionTrade
from collections import defaultdict
import MetaTrader5 as mt5

__all__ = ["aggregate_trades_by_position"]

_DEAL_IN = getattr(mt5, "DEAL_ENTRY_IN", 0)
_DEAL_OUT = getattr(mt5, "DEAL_ENTRY_OUT", 1)


def aggregate_trades_by_position(trades: list[MT5Trade]) -> list[MT5PositionTrade]:
    ordered = sorted(trades, key=lambda t: (t.time_msc, t.ticket))

    by_pid: dict[int, list[MT5Trade]] = defaultdict(list)
    standalone: list[MT5PositionTrade] = []

    for deal in ordered:
        if deal.position_id == 0:
            standalone.append(
                MT5PositionTrade(
                    position_id=0,
                    symbol=deal.symbol or "",
                    standalone=deal,
                )
            )
        else:
            by_pid[deal.position_id].append(deal)

    grouped: list[MT5PositionTrade] = []

    for pid in sorted(by_pid.keys()):
        group = sorted(by_pid[pid], key=lambda t: (t.time_msc, t.ticket))
        closes: list[MT5Trade] = []
        opens: list[MT5Trade] = []
        other: list[MT5Trade] = []

        for d in group:
            if d.entry == _DEAL_IN:
                opens.append(d)
            elif d.entry == _DEAL_OUT:
                closes.append(d)
            else:
                other.append(d)
        
        symbol = next((d.symbol for d in group if d.symbol), "")

        grouped.append(
            MT5PositionTrade(
                position_id=pid,
                symbol=symbol,
                opens=opens,
                closes=closes,
                other_deals=other,
            )
        )

    def sort_key(row: MT5PositionTrade) -> tuple[int, int]:
        if row.standalone is not None:
            return (row.standalone.time_msc, row.standalone.ticket)
        
        first_candidates = row.opens + row.closes + row.other_deals

        if not first_candidates:
            return (0, 0)
        
        first = first_candidates[0]
        return (first.time_msc, first.ticket)

    return sorted(standalone + grouped, key=sort_key)
