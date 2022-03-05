from datetime import date, timedelta

from chalicelib.scraper.search_flights import search_flights


def test_krakow_eindhoven():
    flights = search_flights(
        num_people=1,
        flight_date=date.today() + timedelta(days=7),
        origin_iata="KRK",
        destination_iata="EIN",
    )
    assert 1 <= len(flights) <= 3  # there's almost certainly 1-3 flights


def test_krakow_krakow():
    flights = search_flights(
        num_people=1,
        flight_date=date.today() + timedelta(days=7),
        origin_iata="KRK",
        destination_iata="KRK",
    )
    assert len(flights) == 0
