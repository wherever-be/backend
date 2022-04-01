from datetime import datetime

from backend.apis import world
from backend.connection import Connection
from backend.friend import Friend
from backend.journey import Journey
from backend.price import Price
from backend.search.pick_varied import pick_varied
from backend.trip import Trip


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
