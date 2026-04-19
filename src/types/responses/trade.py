from dataclasses import dataclass, field
from .base import ResponseModel

__all__ = ["MT5Trade", "MT5PositionTrade"]

@dataclass
class MT5Trade(ResponseModel):
    commission: float
    position_id: int
    external_id: str
    profit: float
    time_msc: int
    volume: float
    comment: str
    price: float
    entry: int
    fee: float
    magic: int
    order: int
    reason: int
    swap: float
    symbol: str
    ticket: int
    type: int
    time: int

@dataclass
class MT5PositionTrade(ResponseModel):
    position_id: int
    symbol: str
    opens: list[MT5Trade] = field(default_factory=list)
    closes: list[MT5Trade] = field(default_factory=list)
    other_deals: list[MT5Trade] = field(default_factory=list)
    standalone: MT5Trade | None = None
