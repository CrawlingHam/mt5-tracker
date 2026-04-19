from .trade import MT5PositionTrade, MT5Trade
from .position import MT5Position
from dataclasses import dataclass
from .account import MT5Account
from .base import ResponseModel
from .health import MT5Health

__all__ = ["MT5AllResponse"]

@dataclass
class MT5AllResponse(ResponseModel):
    trades: list[MT5Trade] | list[MT5PositionTrade]
    positions: list[MT5Position]
    account: MT5Account | None
    health: MT5Health
