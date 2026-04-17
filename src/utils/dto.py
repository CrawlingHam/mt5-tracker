from dataclasses import fields
from src.types.alias import T

__all__ = ["to_dataclass"]

def to_dataclass(cls: type[T], data: dict) -> T:
    allowed_fields = {f.name for f in fields(cls)}
    filtered = {key: value for key, value in data.items() if key in allowed_fields}
    return cls(**filtered)