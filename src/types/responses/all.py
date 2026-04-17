from .position import MT5Position
from dataclasses import dataclass
from .account import MT5Account
from .base import ResponseModel
from .health import MT5Health
from .trade import MT5Trade

__all__ = ["MT5AllResponse"]

@dataclass
class MT5AllResponse(ResponseModel):
    positions: list[MT5Position]
    account: MT5Account | None
    trades: list[MT5Trade]
    health: MT5Health
