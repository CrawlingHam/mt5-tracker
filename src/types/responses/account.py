from dataclasses import dataclass
from .base import ResponseModel

__all__ = ["MT5Account"]

@dataclass
class MT5Account(ResponseModel):
    margin_maintenance: float
    commission_blocked: float
    margin_initial: float
    margin_so_call: float
    currency_digits: int
    margin_so_so: float
    margin_level: float
    margin_so_mode: int
    trade_allowed: bool
    margin_free: float
    liabilities: float
    trade_expert: bool
    limit_orders: int
    fifo_close: bool
    margin_mode: int
    trade_mode: int
    balance: float
    assets: float
    credit: float
    currency: str
    equity: float
    leverage: int
    margin: float
    profit: float
    company: str
    server: str
    login: int
    name: str