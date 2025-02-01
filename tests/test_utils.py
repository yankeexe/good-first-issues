import datetime

import pytest

from good_first_issues.utils import parse_period


# Fixture to mock the current time for consistent testing
@pytest.fixture
def mock_datetime_now(monkeypatch):
    # Define a fixed datetime for testing
    fixed_datetime = datetime.datetime(
        2023, 10, 1, 12, 0, 0, tzinfo=datetime.timezone.utc
    )

    # Mock the `datetime.datetime.now` method
    class MockDateTime(datetime.datetime):
        @classmethod
        def now(cls, tz=None):
            return fixed_datetime

    # Replace the real `datetime.datetime` with our mock
    monkeypatch.setattr(datetime, "datetime", MockDateTime)


@pytest.mark.parametrize(
    "duration, expected_period, expected_timedelta",
    [
        ("10m", 10, datetime.timedelta(minutes=10)),
        ("5min", 5, datetime.timedelta(minutes=5)),
        ("15mins", 15, datetime.timedelta(minutes=15)),
        ("30minutes", 30, datetime.timedelta(minutes=30)),
        ("2h", 120, datetime.timedelta(hours=2)),
        ("3hr", 180, datetime.timedelta(hours=3)),
        ("4hrs", 240, datetime.timedelta(hours=4)),
        ("5hours", 300, datetime.timedelta(hours=5)),
        ("1d", 1440, datetime.timedelta(days=1)),
        ("2day", 2880, datetime.timedelta(days=2)),
        ("3days", 4320, datetime.timedelta(days=3)),
    ],
)
def test_parse_period_valid(
    mock_datetime_now, duration, expected_period, expected_timedelta
):
    result = parse_period(duration)
    assert result.absolute_period == expected_period
    assert (
        result.utc_date_time
        == datetime.datetime(2023, 10, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)
        - expected_timedelta
    )


@pytest.mark.parametrize(
    "duration",
    [
        "10",  # Missing duration unit
        "10x",  # Invalid duration unit
        "minutes",  # Missing period
        "-10m",  # Negative period
        "10.5m",  # Non-integer period
    ],
)
def test_parse_period_invalid(duration):
    with pytest.raises(SystemExit):
        parse_period(duration)


def test_parse_period_zero_duration(mock_datetime_now):
    result = parse_period("0m")
    assert result.absolute_period == 0
    assert result.utc_date_time == datetime.datetime(
        2023, 10, 1, 12, 0, 0, tzinfo=datetime.timezone.utc
    )


def test_parse_period_large_duration(mock_datetime_now):
    result = parse_period("1000d")
    assert result.absolute_period == 1000 * 60 * 24
    assert result.utc_date_time == datetime.datetime(
        2023, 10, 1, 12, 0, 0, tzinfo=datetime.timezone.utc
    ) - datetime.timedelta(days=1000)


def test_parse_period_error_message(capsys):
    with pytest.raises(SystemExit):
        parse_period("10x")
    captured = capsys.readouterr()
    assert "❌ Invalid status duration" in captured.err

    with pytest.raises(SystemExit):
        parse_period("10")
    captured = capsys.readouterr()
    assert "Invalid duration" in captured.err
