from datetime import date, timedelta

from chalicelib.geography import Airport
from chalicelib.scraper import rough_connection


def test_krakow_eindhoven():
    flight = rough_connection(
        origin=Airport(name="Krakow", iata="KRK"),
        destination=Airport(name="Eindhoven", iata="EIN"),
        flight_date=date.today() + timedelta(days=7),
    )
    assert flight is not None


def test_krakow_krakow():
    flight = rough_connection(
        origin=Airport(name="Krakow", iata="KRK"),
        destination=Airport(name="Krakow", iata="KRK"),
        flight_date=date.today() + timedelta(days=7),
    )
    assert flight is None
