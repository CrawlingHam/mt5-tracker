from dataclasses import dataclass
from .base import ResponseModel

__all__ = ["MT5Position"]

@dataclass
class MT5Position(ResponseModel):
    time_update_msc: int
    price_current: float
    external_id: str
    price_open: float
    time_update: int
    identifier: int
    profit: float
    time_msc: int
    volume: float
    comment: str
    symbol: str
    ticket: int
    reason: int
    swap: float
    magic: int
    time: int
    type: int
    sl: float
    tp: float