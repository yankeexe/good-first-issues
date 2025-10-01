import datetime
import pytest
from good_first_issues.utils import parse_period, wrap_text_for_table, format_issues_for_display


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


# Tests for text wrapping functionality
class TestTextWrapping:
    """Tests for the new text wrapping functionality added for issue #15."""
    
    def test_wrap_text_for_table_short_text(self):
        """Test that short text is returned unchanged."""
        text = "Short text"
        result = wrap_text_for_table(text, max_width=50)
        assert result == "Short text"
    
    def test_wrap_text_for_table_exact_width(self):
        """Test text exactly at max width."""
        text = "This is exactly fifty characters long text here"
        result = wrap_text_for_table(text, max_width=50)
        assert result == text
        assert len(text) == 50
    
    def test_wrap_text_for_table_word_boundary(self):
        """Test wrapping at word boundaries."""
        text = "This is a very long text that should be wrapped at word boundaries"
        result = wrap_text_for_table(text, max_width=30)
        lines = result.split('\n')
        
        # Check that no line exceeds max width
        for line in lines:
            assert len(line) <= 30
        
        # Check that words are not broken
        assert "This is a very long text that" in lines[0]
        assert "should be wrapped at word" in lines[1]
        assert "boundaries" in lines[2]
    
    def test_wrap_text_for_table_single_long_word(self):
        """Test handling of extremely long words."""
        long_word = "supercalifragilisticexpialidocious" * 2
        result = wrap_text_for_table(long_word, max_width=30)
        
        # Should be truncated with ellipsis
        assert result.endswith("...")
        assert len(result) == 30
    
    def test_wrap_text_for_table_long_url(self):
        """Test handling of long URLs."""
        long_url = "https://github.com/owner/repository/issues/123456789/very-long-issue-title-that-exceeds-normal-length"
        result = wrap_text_for_table(long_url, max_width=30)
        
        # Should be truncated with ellipsis
        assert result.startswith("https://github.com/owner/rep")
        assert result.endswith("...")
        assert len(result) == 30
    
    def test_wrap_text_for_table_mixed_content(self):
        """Test wrapping text with mixed short and long words."""
        text = "Fix supercalifragilisticexpialidocious bug in authentication system"
        result = wrap_text_for_table(text, max_width=25)
        lines = result.split('\n')
        
        # Check that each line is within limit
        for line in lines:
            assert len(line) <= 25
        
        # The long word should be truncated
        assert any("supercalifragilisticexp..." in line for line in lines)
    
    def test_wrap_text_for_table_empty_string(self):
        """Test handling of empty string."""
        result = wrap_text_for_table("", max_width=50)
        assert result == ""
    
    def test_wrap_text_for_table_whitespace_only(self):
        """Test handling of whitespace-only string."""
        result = wrap_text_for_table("   ", max_width=50)
        assert result == "   "
    
    def test_wrap_text_for_table_custom_width(self):
        """Test with custom max width."""
        text = "This is a test for custom width"
        result = wrap_text_for_table(text, max_width=10)
        lines = result.split('\n')
        
        for line in lines:
            assert len(line) <= 10
    
    def test_format_issues_for_display_normal_case(self):
        """Test normal formatting of issues list."""
        issues = [
            ("Fix authentication bug", "https://github.com/owner/repo/issues/1"),
            ("Add new feature for user management", "https://github.com/owner/repo/issues/2")
        ]
        
        result = format_issues_for_display(issues)
        
        assert len(result) == 2
        # Check that titles are preserved (they're short enough)
        assert result[0][0] == "Fix authentication bug"
        assert result[1][0] == "Add new feature for user management"
        # Check that URLs are preserved (they're short enough)
        assert result[0][1] == "https://github.com/owner/repo/issues/1"
        assert result[1][1] == "https://github.com/owner/repo/issues/2"
    
    def test_format_issues_for_display_long_titles(self):
        """Test formatting with long titles that need wrapping."""
        issues = [
            ("This is an extremely long issue title that definitely exceeds the default 50 character limit and should be wrapped appropriately", 
             "https://github.com/owner/repo/issues/1")
        ]
        
        result = format_issues_for_display(issues, title_width=30)
        
        # Title should be wrapped
        wrapped_title = result[0][0]
        lines = wrapped_title.split('\n')
        assert len(lines) > 1
        for line in lines:
            assert len(line) <= 30
    
    def test_format_issues_for_display_long_urls(self):
        """Test formatting with long URLs that need wrapping."""
        issues = [
            ("Short title", 
             "https://github.com/very-long-organization-name/extremely-long-repository-name-that-exceeds-normal-limits/issues/123456789")
        ]
        
        result = format_issues_for_display(issues, url_width=40)
        
        # URL should be wrapped or truncated
        wrapped_url = result[0][1]
        if '\n' in wrapped_url:
            lines = wrapped_url.split('\n')
            for line in lines:
                assert len(line) <= 40
        else:
            # If it's truncated instead of wrapped
            assert len(wrapped_url) <= 40
    
    def test_format_issues_for_display_custom_widths(self):
        """Test formatting with custom column widths."""
        issues = [
            ("This is a moderately long title", "https://github.com/owner/repo/issues/1")
        ]
        
        result = format_issues_for_display(issues, title_width=15, url_width=25)
        
        title_lines = result[0][0].split('\n')
        url_lines = result[0][1].split('\n')
        
        for line in title_lines:
            assert len(line) <= 15
        for line in url_lines:
            assert len(line) <= 25
    
    def test_format_issues_for_display_none_values(self):
        """Test handling of None values in issues."""
        issues = [
            (None, "https://github.com/owner/repo/issues/1"),
            ("Valid title", None),
            (None, None)
        ]
        
        result = format_issues_for_display(issues)
        
        # None values should be replaced with "N/A"
        assert result[0][0] == "N/A"
        assert result[0][1] == "https://github.com/owner/repo/issues/1"
        assert result[1][0] == "Valid title"
        assert result[1][1] == "N/A"
        assert result[2][0] == "N/A"
        assert result[2][1] == "N/A"
    
    def test_format_issues_for_display_empty_list(self):
        """Test handling of empty issues list."""
        result = format_issues_for_display([])
        assert result == []
    
    def test_wrap_text_for_table_edge_cases(self):
        """Test edge cases for text wrapping."""
        # Single character
        assert wrap_text_for_table("A", max_width=1) == "A"
        
        # Text with multiple spaces
        result = wrap_text_for_table("Word1    Word2", max_width=10)
        # Should handle multiple spaces gracefully
        assert "Word1" in result
        assert "Word2" in result
