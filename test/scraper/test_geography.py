from chalicelib.scraper.geography import list_countries


def test_known_countries():
    countries = list_countries()
    assert len([country for country in countries if country.name == "Poland"]) == 1
    assert len([country for country in countries if country.name == "Jupiter"]) == 0
