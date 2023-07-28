import pytest


@pytest.fixture
def number():
    return 1


def test_pytest(number):
    assert 1 == number
