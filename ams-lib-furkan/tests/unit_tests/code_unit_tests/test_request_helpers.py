import pytest
from ams.data_model.common_libs.utils.request_helpers import (
    identify_day_of_ops,
    generate_date_time_data,
)


def test_identify_day_of_ops():
    assert identify_day_of_ops("1234567") == [
        "MON",
        "TUE",
        "WED",
        "THU",
        "FRI",
        "SAT",
        "SUN",
    ]
    assert identify_day_of_ops("135") == ["MON", "WED", "FRI"]
    assert identify_day_of_ops("246") == ["TUE", "THU", "SAT"]
    assert identify_day_of_ops("7") == ["SUN"]
    assert identify_day_of_ops("") == []


def test_generate_date_time_data():
    assert generate_date_time_data("2023-10-05T14:30:00") == (
        ["2023", "10", "05"],
        [14, 30, 0, 0],
    )
    assert generate_date_time_data("2022-01-01T00:00:00") == (
        ["2022", "01", "01"],
        [0, 0, 0, 0],
    )
    assert generate_date_time_data("1999-12-31T23:59:59") == (
        ["1999", "12", "31"],
        [23, 59, 59, 0],
    )
    assert generate_date_time_data("2000-02-29T12:00:00") == (
        ["2000", "02", "29"],
        [12, 0, 0, 0],
    )
