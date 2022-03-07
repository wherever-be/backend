from datetime import date, timedelta

from backend.geography import Airport
from backend.scraper import precise_connections


def test_krakow_eindhoven():
    flights = precise_connections(
        num_people=1,
        flight_date=date.today() + timedelta(days=7),
        origin=Airport(name="Krakow", iata="KRK"),
        destination=Airport(name="Eindhoven", iata="EIN"),
    )
    assert 1 <= len(flights) <= 3  # there's almost certainly 1-3 flights


def test_krakow_krakow():
    flights = precise_connections(
        num_people=1,
        flight_date=date.today() + timedelta(days=7),
        origin=Airport(name="Krakow", iata="KRK"),
        destination=Airport(name="Krakow", iata="KRK"),
    )
    assert len(flights) == 0
