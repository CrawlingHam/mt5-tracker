from datetime import date, datetime, time

__all__ = ["parse_date_param", "resolve_date_range"]

def parse_date_param(value: str, is_end: bool) -> datetime:
    # Date-only input (YYYY-MM-DD): use full-day boundaries.
    if len(value) == 10:
        parsed_date = date.fromisoformat(value)
        return datetime.combine(parsed_date, time.max if is_end else time.min)
    return datetime.fromisoformat(value)


def resolve_date_range(from_date_raw: str | None, to_date_raw: str | None, default_from: datetime = datetime(1999, 1, 1)) -> tuple[datetime, datetime]:
    from_date = parse_date_param(from_date_raw, is_end=False) if from_date_raw else default_from
    if to_date_raw:
        to_date = parse_date_param(to_date_raw, is_end=True)
    elif from_date_raw and len(from_date_raw) == 10:
        to_date = parse_date_param(from_date_raw, is_end=True)
    else:
        to_date = datetime.now()
    return from_date, to_date