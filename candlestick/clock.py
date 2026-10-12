"""Date and time helpers. All times are UTC."""
import datetime


def until_next_day_sec():
    """
    Calculates the time in seconds until the next day (UTC).

    Returns:
        float: Time in seconds until the next day.
    """
    today_utc = datetime.datetime.now(datetime.timezone.utc)
    tomorrow_utc = today_utc + datetime.timedelta(days=1)
    tomorrow_utc = tomorrow_utc.replace(hour=0, minute=0, second=0, microsecond=0)
    time_to_wait = (tomorrow_utc - today_utc).total_seconds()
    return float(time_to_wait)


def today_time():
    """
    Returns the current UTC time in HH:MM:SS format.

    Returns:
        str: Current UTC time.
    """
    today_utc = datetime.datetime.now(datetime.timezone.utc)
    return str(today_utc.strftime('%H:%M:%S'))


def today_date():
    """
    Returns the current day of the week (lowercase).

    Returns:
        str: Current day of the week.
    """
    today_utc = datetime.datetime.now(datetime.timezone.utc).date()
    return str(today_utc.strftime("%A")).lower()


def file_date():
    """
    Returns the current date in YYYY-MM-DD format.

    Returns:
        str: Current date.
    """
    today_utc = datetime.datetime.now(datetime.timezone.utc).date()
    return str(today_utc.strftime("%Y-%m-%d"))


def current_meeting_date():
    """
    Returns a formatted string representing the current date and time (UTC).

    Returns:
        str: Formatted current date and time.
    """
    today_utc = datetime.datetime.now(datetime.timezone.utc).date()
    return str(today_utc.strftime('%A, %B %d, %Y, at 00:00'))
