from src.utils import resolve_origin, split_and_trim
from pathlib import Path
from os import getenv

__all__ = ["allowed_origins"]

def _read_allowed_origins_env() -> str:
    env_value = getenv("ALLOWED_ORIGINS")
    if env_value is not None:
        return env_value

    env_file_path = Path(__file__).resolve().parents[2] / ".env.development"
    if not env_file_path.exists():
        return ""

    for line in env_file_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        if key.strip() == "ALLOWED_ORIGINS":
            return value.strip().strip("\"'")
    return ""


allowed_origins = {resolve_origin(origin) for origin in split_and_trim(_read_allowed_origins_env())}