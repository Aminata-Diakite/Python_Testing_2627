import server


def test_is_past_true_for_old_date():
    assert server.is_past({"date": "2020-01-01 10:00:00"}) is True


def test_is_past_false_for_future_date():
    assert server.is_past({"date": "2999-01-01 10:00:00"}) is False


def test_parse_places_accepts_positive_integer():
    assert server.parse_places("3") == 3


def test_parse_places_rejects_zero():
    assert server.parse_places("0") == 0


def test_parse_places_rejects_negative():
    assert server.parse_places("-2") == 0


def test_parse_places_rejects_text():
    assert server.parse_places("abc") == 0


def test_parse_places_rejects_empty():
    assert server.parse_places("") == 0


def test_parse_places_rejects_none():
    assert server.parse_places(None) == 0


def test_check_booking_ok():
    assert server.check_booking(3, points=13, available=25, already=0) is None


def test_check_booking_not_enough_points():
    assert "points" in server.check_booking(5, points=4, available=25, already=0)


def test_check_booking_not_enough_places():
    assert "places available" in server.check_booking(3, points=13, available=2, already=0)


def test_check_booking_over_limit_single_request():
    assert "12" in server.check_booking(13, points=20, available=25, already=0)


def test_check_booking_over_limit_cumulative():
    assert "12" in server.check_booking(9, points=20, available=25, already=4)


def test_check_booking_exactly_12_ok():
    assert server.check_booking(12, points=13, available=25, already=0) is None


def test_check_booking_all_points_ok():
    assert server.check_booking(4, points=4, available=25, already=0) is None


def test_load_competitions_returns_list_with_names():
    competitions = server.loadCompetitions()
    assert all("name" in c for c in competitions)
