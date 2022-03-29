from datetime import date, datetime, timedelta

from backend import Query
from backend.apis import world
from backend.connection import Connection
from backend.friend import Friend
from backend.journey import Journey
from backend.price import Price
from backend.search import search, pick_varied
from backend.time_frame import TimeFrame
from backend.trip import Trip


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


def test_pick_varied():
    friend = Friend(name="Harold", city=world().city_by_code("PARIS"))
    candidates = [
        Trip(
            destination=world().city_by_code(destination),
            journeys=[
                Journey(
                    friend=friend,
                    home_to_destination=Connection(
                        from_airport=world().airport_by_iata("BVA"),
                        departure=datetime(2013, 7, 1, 13),
                        to_airport=world().airport_by_iata(to_airport),
                        arrival=datetime(2013, 7, 1, 15),
                        price=Price(amount=price, currency="EUR"),
                    ),
                    destination_to_home=Connection(
                        from_airport=world().airport_by_iata(to_airport),
                        departure=datetime(2013, 7, 2, 13),
                        to_airport=world().airport_by_iata("BVA"),
                        arrival=datetime(2013, 7, 2, 15),
                        price=Price(amount=price, currency="EUR"),
                    ),
                )
            ],
        )
        for destination, to_airport, price in [
            ("STOCKHOLM", "ARN", 10),
            ("STOCKHOLM", "ARN", 11),
            ("BARCELONA", "BCN", 12),
        ]
    ]
    picked = pick_varied(candidates, max_trips=2)
    assert len(candidates) == 3  # i.e. pick_varied does not edit the original list
    assert len(picked) == 2
    assert picked[0] == candidates[0]
    assert picked[1] == candidates[2]
