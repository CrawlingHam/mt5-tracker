from pathlib import Path
from os import environ

__all__ = ["load_env_file"]

def load_env_file() -> None:
    env_file_path = Path(__file__).resolve().parents[2] / ".env.development"
    if not env_file_path.exists():
        return

    for line in env_file_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        env_key = key.strip()
        env_value = value.strip().strip("\"'")
        environ.setdefault(env_key, env_value)