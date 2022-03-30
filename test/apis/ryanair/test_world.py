import pytest

from backend.apis.ryanair import world


def test_known_countries():
    assert world().country_by_code("pl").name == "Poland"
    with pytest.raises(Exception):
        world().country_by_code("chihuahua")
