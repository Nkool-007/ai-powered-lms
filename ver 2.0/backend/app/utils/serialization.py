def isoformat_or_none(value):
    if value is None:
        return None
    return value.isoformat()
