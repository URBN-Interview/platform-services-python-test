import pytest

from rewardsservice.utils import email_is_valid, total_is_valid


@pytest.mark.parametrize("email, expected", [
    ("validemail@gmail.com", True),
    ("valid-email@gmail.com", True),
    ("valid.email@gmail.com", True),
    ("invalid.com", False),
    ("123abc", False),
    ("invalid_email@gmail", False)
])
def test_email_is_valid_returns_expected(email, expected):
    assert email_is_valid(email) == expected


@pytest.mark.parametrize("order_total, expected", [
    ("20.50", True),
    ("10", True),
    ("-10", False),
    ("-10.50", False),
    ("0", False),
    ("abc", False),
    ("a1b3", False)
])
def test_email_is_valid_returns_expected(order_total, expected):
    assert total_is_valid(order_total) == expected
