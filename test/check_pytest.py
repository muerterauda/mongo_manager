import pytest


@pytest.fixture
def number():
    return 1


def test_pytest(number):
    assert 1 == number


def test_pytest_2(number):
    assert 2 == number
