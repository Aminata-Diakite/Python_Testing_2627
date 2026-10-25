import pytest

import server


@pytest.mark.parametrize("raw, expected", [
    ("1", 1), ("5", 5), ("12", 12), ("13", 13), (" 7 ", 7),
    ("007", 7), ("+4", 4), ("0", 0), ("-0", 0), ("-1", 0),
    ("-12", 0), ("abc", 0), ("", 0), (" ", 0), (None, 0),
    ("3.5", 0), ("1e2", 0),
])
def test_parse_places_cases(raw, expected):
    assert server.parse_places(raw) == expected


@pytest.mark.parametrize("places, points, available, already, accepted", [
    (1, 13, 25, 0, True),
    (12, 13, 25, 0, True),
    (13, 20, 25, 0, False),
    (4, 4, 25, 0, True),
    (5, 4, 25, 0, False),
    (3, 13, 2, 0, False),
    (2, 13, 2, 0, True),
    (8, 13, 25, 4, True),
    (9, 13, 25, 4, False),
    (1, 13, 25, 11, True),
    (1, 13, 25, 12, False),
    (12, 12, 12, 0, True),
    (1, 0, 25, 0, False),
    (1, 13, 0, 0, False),
    (12, 12, 13, 1, False),
    (6, 6, 6, 6, True),
])
def test_check_booking_cases(places, points, available, already, accepted):
    result = server.check_booking(places, points, available, already)
    assert (result is None) is accepted


@pytest.mark.parametrize("date, expected", [
    ("2020-01-01 10:00:00", True),
    ("1999-12-31 23:59:59", True),
    ("2999-01-01 10:00:00", False),
    ("2500-06-15 08:30:00", False),
    ("2038-01-19 03:14:07", False),
])
def test_is_past_cases(date, expected):
    assert server.is_past({"date": date}) is expected
