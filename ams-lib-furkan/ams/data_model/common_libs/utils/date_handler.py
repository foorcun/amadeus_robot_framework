# pylint: disable=line-too-long

"""
This module provides utility functions for handling dates.
"""

from enum import Enum
from time import gmtime
import datetime
from dateutil.relativedelta import relativedelta

# pylint: disable=unused-variable


def initialize_keyword_arguments(**kwargs):
    """
    Initialize keyword arguments for date and time components.

    Keyword Arguments:
        years (int): Number of years. Default is 0.
        months (int): Number of months. Default is 0.
        weeks (int): Number of weeks. Default is 0.
        days (int): Number of days. Default is 0.
        hours (int): Number of hours. Default is 0.
        minutes (int): Number of minutes. Default is 0.
        seconds (int): Number of seconds. Default is 0.
        microseconds (int): Number of microseconds. Default is 0.
        week_day (int or None): Day of the week. Default is None.
        date (datetime.date or None): Specific date. Default is None.
        time_format (str or None): Format for time. Default is None.
        date_format (DateFormat): Format for date. Default is DateFormat.DATE.

    Returns:
        tuple: A tuple containing the initialized values for years, months, weeks, days, hours, minutes, seconds, microseconds, week_day, date, time_format, and date_format.
    """
    years = kwargs.get("years", 0)
    months = kwargs.get("months", 0)
    weeks = kwargs.get("weeks", 0)
    days = kwargs.get("days", 0)
    hours = kwargs.get("hours", 0)
    minutes = kwargs.get("minutes", 0)
    seconds = kwargs.get("seconds", 0)
    microseconds = kwargs.get("microseconds", 0)
    week_day = kwargs.get("week_day", None)
    date = kwargs.get("date", None)
    time_format = kwargs.get("time_format", None)
    date_format = kwargs.get("date_format", DateFormat.DATE)
    return (
        years,
        months,
        weeks,
        days,
        hours,
        minutes,
        seconds,
        microseconds,
        week_day,
        date,
        time_format,
        date_format,
    )


class DateFormat(str, Enum):
    """
    DateFormat is an enumeration of various date and datetime string formats.
    Attributes:
        DATE (str): Format for date in the form 'YYYY-MM-DD' (e.g., '2020-12-31').
        DATE_NO_DASH (str): Format for date without dashes in the form 'YYYYMMDD'
          (e.g., '20201231').
        DATETIME (str): Format for datetime in the form 'YYYY-MM-DDTHH:MM:SSZ'
        (e.g., '2020-12-31T23:59:59Z').
        DATETIME_NO_Z (str): Format for datetime without 'Z' in the form
        'YYYY-MM-DDTHH:MM:SS' (e.g., '2020-12-31T23:59:59').
        DATETIME_STR (str): Format for datetime with microseconds in the form
          'YYYY-MM-DD HH:MM:SS.ffffff' (e.g., '2020-12-31 23:59:59.000000').
        DAY_MONTH (str): Format for day and abbreviated month in the form 'DDMMM' (e.g., '31Dec').
        DATE_DMY (str): Format for date in the form 'DDMMYYYY' (e.g., '31122020').
        MONTH_DAY (str): Format for month and day in the form 'MM-DD' (e.g., '12-31').
        DATE_MONTH_YEAR (str): Format for date with uppercase abbreviated month
        in the form 'DD^MMMYYYY' (e.g., '31JAN2020').
    """

    DATE = "%Y-%m-%d"  # 2020-12-31
    DATE_NO_DASH = "%Y%m%d"  # 20201231
    DATETIME = "%Y-%m-%dT%H:%M:%SZ"  # 2020-12-31T23:59:59Z
    DATETIME_NO_Z = "%Y-%m-%dT%H:%M:%S"  # 2020-12-31T23:59:59
    DATETIME_STR = "%Y-%m-%d %H:%M:%S.%f"  # 2020-12-31 23:59:59.000000
    DAY_MONTH = "%d%b"  # 31Dec
    DATE_DMY = "%d%m%Y"  # 31122020
    MONTH_DAY = "%m-%d"  # 12-31
    DATE_MONTH_YEAR = "%d%^b%Y"  # 31JAN2020


class WeekDay(int, Enum):
    """
    WeekDay is an enumeration that represents the days of the week.

    Attributes:
        MON (int): Represents Monday.
        TUE (int): Represents Tuesday.
        WED (int): Represents Wednesday.
        THU (int): Represents Thursday.
        FRI (int): Represents Friday.
        SAT (int): Represents Saturday.
        SUN (int): Represents Sunday.
    """

    MON = 0
    TUE = 1
    WED = 2
    THU = 3
    FRI = 4
    SAT = 5
    SUN = 6


# pylint: disable=too-many-locals


def get_date(**kwargs):
    """
    Get a date relative to the given date and format it to the given format.
      - date: the reference date and can have the following values:
        - None: use now in GMT time so all relative time (hours, minutes, seconds,
          microseconds) would be from current time
        - date/datetime string: it will try to convert it to a real date object through all
          DateFormat
        - lambda/function: call it, it should return a date or datetime object
        - today_gmt: will get the current date without current time so all relative time
        (hours, minutes, seconds, microseconds) would be from 00:00:00
        - date/datetime object: just use it
      - week_day: if not None, the reference date will become the next given week day
      after the reference date
      - years, months, weeks, days, hours, minutes, seconds, microseconds: positive or
      negative integer to give a relative date from the reference one
      - date_format: the format in which to format the date, can be the following values:
        - None: return a datetime object
        - str/lamda/function: use the given function to format
        - DateFormat: format following the given format
    Examples:
      Lets assume that current datetime is 2020-12-25 14:30:45
      get_date(hours=6) --> 2020-12-25
      get_date(years=-5, hours=-6, date_format=DateFormat.DATETIME) --> 2015-12-25T08:30:45Z
      get_date(hours=6, date_format=DateFormat.DATETIME) --> 2020-12-25T20:30:45Z
      get_date(hours=6, date=today_gmt, date_format=DateFormat.DATETIME) --> 2020-12-25T06:00:00Z
      get_date(hours=6, date='2020-12-25', date_format=DateFormat.DATETIME) -->
        2020-12-25T06:00:00Z
    """

    (
        years,
        months,
        weeks,
        days,
        hours,
        minutes,
        seconds,
        microseconds,
        week_day,
        date,
        time_format,
        date_format,
    ) = initialize_keyword_arguments(**kwargs)
    print(week_day)
    if date is None:
        base_date = now_gmt()
    elif isinstance(date, str):
        base_date = str_to_date(date)
    elif callable(date):
        base_date = date()
    else:
        base_date = date
    if week_day is not None:
        base_date = next_week_day(week_day, base_date)

    result = base_date + relativedelta(
        years=years,
        months=months,
        weeks=weeks,
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
        microseconds=microseconds,
    )

    if time_format:
        time_parts = list(map(int, time_format.split(":")))
        result = result.replace(
            hour=time_parts[0],
            minute=time_parts[1] if len(time_parts) > 1 else 0,
            second=time_parts[2] if len(time_parts) > 2 else 0,
            microsecond=time_parts[3] if len(time_parts) > 3 else 0,
        )

    if date_format is None:
        return result
    if callable(date_format):
        return date_format(result)
    if date_format == str:
        return str(result)
    return result.strftime(date_format)


def today_gmt():
    """Return GMT today date"""
    return datetime.date(gmtime().tm_year, gmtime().tm_mon, gmtime().tm_mday)


def now_gmt():
    """Return GMT today datetime"""
    return datetime.datetime.utcnow()


def next_week_day(week_day=0, date=None):
    """
    Give the next given week day from given date (default is next Monday from now).
    WeekDay: 0=Monday, 1=Tuesday, 2=Wednesday, 3=Thursday, 4=Friday, 5=Saturday, 6=Sunday
    """
    if week_day < 0 or week_day > 6:
        raise ValueError(
            f'Weekday must be between 0 (Monday) and 6 (Sunday): "{week_day}" is not valid'
        )
    if not date:
        date = today_gmt()

    days_ahead = week_day - date.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return date + datetime.timedelta(days=days_ahead)


def str_to_date(date):
    """Transform the given date"""
    for date_format in DateFormat:
        try:
            return datetime.datetime.strptime(date, date_format.value)
        except ValueError:
            pass
    raise ValueError(f'Unable to transform "{date}" into a date')


def relative_date(**kwargs):
    """Get a relative date from the given date"""
    (
        years,
        months,
        weeks,
        days,
        hours,
        minutes,
        seconds,
        microseconds,
        week_day,
        date,
        time_format,
        date_format,
    ) = initialize_keyword_arguments(**kwargs)
    return (date if date is not None else today_gmt()) + relativedelta(
        years=years,
        months=months,
        weeks=weeks,
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
        microseconds=microseconds,
    )


def relative_date_str(**kwargs):
    """Get a relative date string from the given date"""
    (
        years,
        months,
        weeks,
        days,
        hours,
        minutes,
        seconds,
        microseconds,
        week_day,
        date,
        time_format,
        date_format,
    ) = initialize_keyword_arguments(**kwargs)

    result = relative_date(
        years=years,
        months=months,
        weeks=weeks,
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
        microseconds=microseconds,
        date=date,
    )
    if date_format is None:
        return str(result)
    return relative_date(
        years=years,
        months=months,
        weeks=weeks,
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
        microseconds=microseconds,
        date=date,
    ).strftime(date_format)


def next_week_day_str(week_day=0, date=None, date_format=None):
    """Get the next week day string from the given date"""
    return relative_date_str(
        date=next_week_day(week_day, date), date_format=date_format
    )


def convert_to_date(date_, format_):
    """Convert a string to a date object"""
    return datetime.datetime.strptime(date_, format_)


def calculate_age(birth_date, format_, travel_date):
    """Calculate age based on birth date and travel date"""
    birth_date = convert_to_date(birth_date, format_)
    today_ = convert_to_date(travel_date, format_)
    age = (
        today_.year
        - birth_date.year
        - ((today_.month, today_.day) < (birth_date.month, birth_date.day))
    )
    return age


def get_dates_between(start, end):
    """Store all dates between start date and end date and return as a list"""
    from datetime import datetime, timedelta

    start = datetime.strptime(start, "%Y%m%d")
    end = datetime.strptime(end, "%Y%m%d")
    op_dates = [
        (start + timedelta(days=i)).strftime("%Y%m%d")
        for i in range((end - start).days + 1)
    ]
    return op_dates
