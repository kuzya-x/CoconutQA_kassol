import pytest
import conftest
from conftest import created_movie, auth_session


@pytest.mark.skip(reason="Временно отключён")
def test_skip():
    assert True


@pytest.mark.skipif(None, reason="Тест в разработке")
def test_skipif():
    assert True

@pytest.mark.xfail(reason="Функция в разработка")
def test_xfail():
    assert False

@pytest.fixture
def setup_data():
    print("Setup")

@pytest.mark.usefixtures('setup_data')
def test_usefixtures():
    assert True

import pytest

@pytest.mark.smoke
def test_addition():
    assert 1 + 1 == 2

@pytest.mark.regression
def test_subtraction():
    assert 5 - 3 == 2

@pytest.mark.api
def test_multiplication():
    assert 2 * 3 == 6

@pytest.mark.db
def test_division():
    assert 10 / 2 == 5