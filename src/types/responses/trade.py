from dataclasses import dataclass
from .base import ResponseModel

__all__ = ["MT5Trade"]

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