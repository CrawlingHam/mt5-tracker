from flask import Blueprint, Response, jsonify
from src.utils import to_dataclass
from dataclasses import asdict
from src.types import MT5Account
from src.routes import init_mt5
import MetaTrader5 as mt5

account_bp = Blueprint("account", __name__)

@account_bp.route("/account")
def account() -> Response:
    init_mt5()

    account_info = mt5.account_info()

    if not account_info:
        return jsonify(None)

    account_response = to_dataclass(MT5Account, account_info._asdict())
    return jsonify(asdict(account_response))
