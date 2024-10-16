from datetime import datetime, timedelta


def today() -> datetime:
    "Get today datetime instance"
    return datetime.now().date()


def today_str() -> str:
    "Get today's in YYYY-MM-DD format"
    return today().strftime("%Y-%m-%d")


def date_from(time_delta: timedelta) -> str:
    "Get a certain date in the past on specific interval from today in YYYY-MM-DD format"
    past_date = today() - time_delta
    return past_date.strftime("%Y-%m-%d")
