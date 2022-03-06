from chalicelib.scraper.world import world


def test_known_countries():
    world = world()
    assert len([country for country in countries if country.name == "Poland"]) == 1
    assert len([country for country in countries if country.name == "Jupiter"]) == 0
