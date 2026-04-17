from .origins import __all__ as _origins_all
from src.utils import load_env_file
from pathlib import Path
from .origins import *
import importlib.util

load_env_file()

_global_constants_path = Path(__file__).with_name("global.constants.py")
_global_constants_spec = importlib.util.spec_from_file_location(
    "src.configs.global_constants_file", _global_constants_path
)
_global_constants_module = importlib.util.module_from_spec(_global_constants_spec)
assert _global_constants_spec is not None and _global_constants_spec.loader is not None
_global_constants_spec.loader.exec_module(_global_constants_module)

PORT = _global_constants_module.PORT
IS_PRODUCTION = _global_constants_module.IS_PRODUCTION

__all__ = [*_origins_all, "IS_PRODUCTION", "PORT"]