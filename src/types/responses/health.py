from dataclasses import dataclass
from .base import ResponseModel

__all__ = ["MT5Health", "MT5Terminal"]

@dataclass
class MT5Terminal(ResponseModel):
    notifications_enabled: bool
    community_connection: bool
    community_balance: float
    community_account: bool
    tradeapi_disabled: bool
    retransmission: float
    commondata_path: str
    email_enabled: bool
    trade_allowed: bool
    dlls_allowed: bool
    ftp_enabled: bool
    connected: bool
    data_path: str
    ping_last: int
    codepage: int
    language: str
    company: str
    maxbars: int
    build: int
    mqid: bool
    name: str
    path: str

@dataclass
class MT5Health(ResponseModel):
    connected: bool
    terminal: MT5Terminal