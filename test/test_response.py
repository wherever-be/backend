from datetime import datetime

from chalicelib import Response
from chalicelib.connection import Connection
from chalicelib.friend import Friend
from chalicelib.journey import Journey
from chalicelib.price import Price
from chalicelib.scraper import world
from chalicelib.trip import Trip


def test_to_frontend_json():
    response = Response(
        trips=[
            Trip(
                destination=world().city_by_code("ROME"),
                journeys=[
                    Journey(
                        friend=Friend(name="Josh", city=world().city_by_code("BERLIN")),
                        home_to_destination=Connection(
                            from_airport=world().airport_by_iata("BER"),
                            departure=datetime(2022, 3, 5, 12, 57),
                            to_airport=world().airport_by_iata("CIA"),
                            arrival=datetime(2022, 3, 5, 14, 29),
                            price=Price(amount=64, currency="EUR"),
                        ),
                        destination_to_home=Connection(
                            from_airport=world().airport_by_iata("FCO"),
                            departure=datetime(2022, 3, 9, 11, 13),
                            to_airport=world().airport_by_iata("BER"),
                            arrival=datetime(2022, 3, 9, 13, 00),
                            price=Price(amount=78, currency="SEK"),
                        ),
                    )
                ],
            )
        ]
    )
    trip = response.frontend_json["searchResults"][0]
    assert trip["destination"] == "ROME"
    journey = trip["journeys"][0]
    assert journey["friendName"] == "Josh"
    assert journey["staysHome"] == False
    assert journey["homeToDest"]["departure"]["date"] == "2022-03-05T12:57:00"
    assert journey["homeToDest"]["departure"]["port"] == "BER"
    assert journey["homeToDest"]["arrival"]["date"] == "2022-03-05T14:29:00"
    assert journey["homeToDest"]["arrival"]["port"] == "CIA"
    assert journey["homeToDest"]["price"]["amount"] == 64
    assert journey["homeToDest"]["price"]["currency"] == "EUR"
    assert journey["homeToDest"]["bookingLink"].startswith("https://www.ryanair.com")
    assert journey["destToHome"]["departure"]["date"] == "2022-03-09T11:13:00"
    assert journey["destToHome"]["departure"]["port"] == "FCO"
    assert journey["destToHome"]["arrival"]["date"] == "2022-03-09T13:00:00"
    assert journey["destToHome"]["arrival"]["port"] == "BER"
    assert journey["destToHome"]["price"]["currency"] == "EUR"
    assert journey["destToHome"]["bookingLink"].startswith("https://www.ryanair.com")
