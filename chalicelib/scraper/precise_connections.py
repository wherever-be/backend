from cachetools import cached, TTLCache
from datetime import date, datetime
from typing import List

from chalicelib.connection import Connection
from chalicelib.geography import Airport
from chalicelib.price import Price
from .ryanair import make_request, RyanairAPIError


@cached(cache=TTLCache(maxsize=65536, ttl=24 * 60 * 60))
def precise_connections(
    num_people: int, flight_date: date, origin: Airport, destination: Airport
) -> List[Connection]:
    """All connections on a given day, with exact prices"""
    try:
        response = make_request(
            "https://www.ryanair.com/api/booking/v4/en-gb/availability",
            parameters=dict(
                ADT=num_people,  # number of adults
                TEEN=0,  # number of 12-15 year olds
                CHD=0,  # number of 2-11 year olds
                INF=0,  # number of <2 year olds
                DateIn="",  # empty for one-way
                DateOut=flight_date.isoformat(),
                Origin=origin.iata,
                Destination=destination.iata,
                Disc=0,  # no idea what this is
                promoCode="",
                IncludeConnectingFlights=False,
                FlexDaysBeforeOut=0,
                FlexDaysOut=0,  # TODO: this can be up to 6, then we get results for later dates as well
                ToUs="AGREED",
            ),
        )
    except RyanairAPIError as api_error:
        if api_error.code == 404:
            return []  # no connecting flights
        raise api_error
    flights = response["trips"][0]["dates"][0]["flights"]
    return [
        Connection(
            from_airport=origin,
            departure=datetime.fromisoformat(flight["segments"][0]["time"][0]),
            to_airport=destination,
            arrival=datetime.fromisoformat(flight["segments"][-1]["time"][-1]),
            price=Price(
                amount=flight["regularFare"]["fares"][0]["amount"],
                currency=response["currency"],
            ),
        )
        for flight in flights
    ]