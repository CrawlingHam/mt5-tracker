__all__ = ["split_and_trim", "resolve_origin"]

def split_and_trim(input_value: str) -> list[str]:
    return [part.strip() for part in input_value.split(",") if part.strip()]


def resolve_origin(origin: str) -> str:
    if origin.startswith("http://") or origin.startswith("https://"):
        return origin
    if "." in origin and not origin.startswith("localhost"):
        return f"https://{origin}"
    return origin