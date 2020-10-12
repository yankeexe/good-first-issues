import pytest

from good_first_issues.utils import identify_limit
from good_first_issues.utils import get_row_ids


@pytest.mark.parametrize(
    "limit, all, expected",
    [(50, False, 50), (None, False, 10), (None, True, None), (50, True, 50)],
)
def test_identify_limit(limit, all, expected):
    """
    Check correctness of `limiter` value returned.
    """
    assert identify_limit(limit, all) == expected


@pytest.mark.parametrize(
    "issues, limiter, expected",
    [(10, None, list(range(1, 11))), (100, 10, list(range(1, 11)))],
)
def test_get_row_ids(issues, limiter, expected):
    """
    Check correctness of iterable returned.
    """
    assert get_row_ids(issues, limiter) == expected
