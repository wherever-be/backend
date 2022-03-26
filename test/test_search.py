from datetime import date, timedelta

from backend import Query, search
from backend.apis import world
from backend.time_frame import TimeFrame
from backend.friend import Friend


def test_simple_search():
    query = Query(
        time_frame=TimeFrame(
            start_date=date.today(), end_date=date.today() + timedelta(days=14)
        ),
        min_days=3,
        max_days=7,
        friends=[
            Friend(
                name="Jake",
                city=world().city_by_code("KRAKOW"),
            )
        ],
        destination_country=world().country_by_code("nl"),
        destination_city=world().city_by_code("EINDHOVEN"),
    )
    results = search(query)
    assert len(results.trips) >= 1
    assert results.trips[0].destination.name == "Eindhoven"
    assert results.trips[0].journeys[0].friend.name == "Jake"
    assert results.trips[0].journeys[0].home_to_destination.from_airport.iata == "KRK"
    assert results.trips[0].journeys[0].home_to_destination.to_airport.iata == "EIN"
    assert results.trips[0].journeys[0].destination_to_home.from_airport.iata == "EIN"
    assert results.trips[0].journeys[0].destination_to_home.to_airport.iata == "KRK"
