import pytest
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from time import gmtime

from ams.data_model.common_libs.utils.date_handler import (
    get_date,
    today_gmt,
    now_gmt,
    next_week_day,
    str_to_date,
    convert_to_date,
    calculate_age,
    DateFormat,
    WeekDay,
)


def test_get_date_default():
    result = get_date()
    assert result == now_gmt().strftime(DateFormat.DATE.value)


def test_get_date_with_hours():
    result = get_date(hours=6, date_format=DateFormat.DATETIME)
    expected = now_gmt() + relativedelta(hours=6)
    assert result == expected.strftime(DateFormat.DATETIME.value)


def test_get_date_with_date_string():
    result = get_date(date="2020-12-25", date_format=DateFormat.DATETIME)
    expected = datetime(2020, 12, 25)
    assert result == expected.strftime(DateFormat.DATETIME.value)


def test_get_date_with_weekDay():
    result = get_date(
        week_day=WeekDay.MON, date="2020-12-25", date_format=DateFormat.DATE
    )
    expected = datetime(2020, 12, 28)
    assert result == expected.strftime(DateFormat.DATE.value)


def test_today_gmt():
    result = today_gmt()
    expected = date(gmtime().tm_year, gmtime().tm_mon, gmtime().tm_mday)
    assert result == expected


def test_now_gmt():
    result = now_gmt()
    expected = datetime.utcnow()
    assert result.strftime(DateFormat.DATETIME.value) == expected.strftime(
        DateFormat.DATETIME.value
    )


def test_next_week_day():
    result = next_week_day(WeekDay.MON, date(2020, 12, 25))
    expected = date(2020, 12, 28)
    assert result == expected


def test_str_to_date():
    result = str_to_date("2020-12-25")
    expected = datetime(2020, 12, 25)
    assert result == expected


def test_convert_to_date():
    result = convert_to_date("2020-12-25", DateFormat.DATE.value)
    expected = datetime(2020, 12, 25)
    assert result == expected


def test_calculate_age():
    result = calculate_age("1990-12-25", DateFormat.DATE.value, "2020-12-25")
    expected = 30
    assert result == expected


def test_str_to_date():
    today = datetime(2020, 12, 25)
    today_time = datetime(2020, 12, 25, 23, 59, 59)
    assert str_to_date("2020-12-25") == today
    assert str_to_date("20201225") == today
    assert str(str_to_date("2020-12-25T23:59:59Z")) == str(today_time)


def test_get_date():
    today = datetime(2020, 12, 25)
    today_time = datetime(2020, 12, 25, 23, 59, 59)
    assert get_date(date=today, date_format=None) == today
    assert get_date(date="2020-12-25", date_format=None) == today
    assert get_date(date="2020-12-25T00:00:00Z", date_format=None) == today
    assert get_date(date="2020-12-25T23:59:59Z", date_format=None) == today_time
    assert get_date(date=today, date_format=lambda x: str(x)) == "2020-12-25 00:00:00"
    assert get_date(date=today, date_format=str) == "2020-12-25 00:00:00"
    assert get_date(date=today, date_format=DateFormat.DATE) == "2020-12-25"
    assert get_date(date=today, date_format=DateFormat.DATE_DMY) == "25122020"
    assert (
        get_date(date=today, date_format=DateFormat.DATETIME) == "2020-12-25T00:00:00Z"
    )
    assert (
        get_date(date=today_time, date_format=DateFormat.DATETIME_STR)
        == "2020-12-25 23:59:59.000000"
    )
    assert (
        get_date(date=today_time, date_format=DateFormat.DATETIME)
        == "2020-12-25T23:59:59Z"
    )
    assert (
        get_date(date=today_time, date_format=DateFormat.DATETIME_NO_Z)
        == "2020-12-25T23:59:59"
    )
    assert (
        get_date(week_day=WeekDay.MON, date=today, date_format=DateFormat.DATE)
        == "2020-12-28"
    )
    assert (
        get_date(days=-1, week_day=WeekDay.MON, date=today, date_format=DateFormat.DATE)
        == "2020-12-27"
    )
    assert (
        get_date(days=1, week_day=WeekDay.MON, date=today, date_format=DateFormat.DATE)
        == "2020-12-29"
    )
    assert (
        get_date(months=-1, date="2020-12-31", date_format=DateFormat.DATETIME_STR)
        == "2020-11-30 00:00:00.000000"
    )
    assert (
        get_date(
            years=-2,
            months=-3,
            hours=-11,
            minutes=-3,
            seconds=-2,
            microseconds=-111,
            week_day=WeekDay.THU,
            date="2020-12-25 22:33:44.123456",
            date_format=DateFormat.DATETIME_STR,
        )
        == "2018-09-30 11:30:42.123345"
    )
