from datetime import datetime
from functools import lru_cache
from typing import Optional, List

import dateutil
import pytz


@lru_cache(maxsize=128)
def try_parse_datetime(datetime_str: str) -> Optional[datetime]:
    """
    Parse a date string into a datetime object.

    This function attempts to parse the input string using dateutil.parser first,
    and if that fails, it tries a series of common date formats.

    Args:
        datetime_str (str): The date string to parse.

    Returns:
        Optional[datetime]: A datetime object in UTC timezone if parsing is successful, None otherwise.
    """
    # First, try to parse with dateutil
    try:
        dt: datetime = dateutil.parser.parse(datetime_str)
        return dt.astimezone(pytz.UTC)
    except (ValueError, OverflowError, dateutil.parser.ParserError):
        date_formats: List[str] = [
            "%Y-%m-%d",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%B %d, %Y",
            "%b %d, %Y",
            "%d %B %Y",
            "%d %b %Y",
            "%Y/%m/%d",
            "%m/%d/%Y",
            "%d/%m/%Y",
        ]
        for fmt in date_formats:
            try:
                return datetime.strptime(datetime_str, fmt).replace(tzinfo=pytz.UTC)
            except ValueError:
                continue
    return None
