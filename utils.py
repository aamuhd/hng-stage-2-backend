from datetime import datetime, timezone


def get_utc_timestamp():
    return datetime.now(timezone.utc)


