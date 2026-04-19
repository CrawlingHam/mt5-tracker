from dataclasses import dataclass
from .base import ResponseModel

__all__ = ["MT5PairStats", "MT5PairsResponse"]

@dataclass
class MT5PairStats(ResponseModel):
    trade_percentage: float
    trade_count: int
    symbol: str

@dataclass
class MT5PairsResponse(ResponseModel):
    pairs: list[MT5PairStats]
    total_trades: int
