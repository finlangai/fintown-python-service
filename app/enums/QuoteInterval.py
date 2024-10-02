from enum import Enum


class QuoteInterval(Enum):
    """Only Four interval type because they often have stable quotes data"""

    MINUTELY = 0
    HOURLY = 4
    DAILY = 5
    WEEKLY = 6
    MONTHLY = 7
