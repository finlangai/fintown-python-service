from datetime import datetime, timedelta, timezone


def today() -> datetime:
    "Get today datetime instance in UTC"
    return datetime.now(timezone.utc).date()


def today_str() -> str:
    "Get today's date in YYYY-MM-DD format in UTC"
    return today().strftime("%Y-%m-%d")


def date_from(time_delta: timedelta) -> str:
    "Get a certain date in the past on specific interval from today in YYYY-MM-DD format in UTC"
    past_date = today() - time_delta
    return past_date.strftime("%Y-%m-%d")


def iso_now() -> str:
    "Get current ISO format datetime in UTC"
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%SZ")
