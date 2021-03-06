from datetime import date, timedelta

from backend.apis.ryanair import rough_connections
from backend.geography import Airport


def test_krakow_eindhoven():
    flights = rough_connections(
        origin=Airport(name="Krakow", iata="KRK"),
        destination=Airport(name="Eindhoven", iata="EIN"),
        flight_date=date.today() + timedelta(days=7),
    )
    assert len(flights) == 1


def test_krakow_krakow():
    flights = rough_connections(
        origin=Airport(name="Krakow", iata="KRK"),
        destination=Airport(name="Krakow", iata="KRK"),
        flight_date=date.today() + timedelta(days=7),
    )
    assert len(flights) == 0
