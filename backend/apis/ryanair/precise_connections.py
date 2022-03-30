from datetime import date, datetime, timedelta
from tenacity import retry, retry_if_exception, wait_exponential
from typing import List

from backend.caching import expiring_cache
from backend.connection import Connection
from backend.geography import Airport
from backend.price import Price
from .connected_airports import connected_airports
from .errors import RyanairAPIError
from .make_request import make_request


def precise_connections(
    num_people: int, flight_date: date, origin: Airport, destination: Airport
):
    rounded_day = ((flight_date.day - 1) // 7) * 7 + 1
    week_start = date(year=flight_date.year, month=flight_date.month, day=rounded_day)
    weekly_connections = _precise_connections(
        num_people=num_people,
        start_date=week_start,
        origin=origin,
        destination=destination,
    )
    return [
        connection
        for connection in weekly_connections
        if connection.departure.date() == flight_date
    ]


@expiring_cache(duration=timedelta(hours=6))
@retry(
    retry=retry_if_exception(
        lambda exception: isinstance(exception, RyanairAPIError)
        and exception.code == 404  # mr Ryan put us on his naughty list
    ),
    wait=wait_exponential(),
)
def _precise_connections(
    num_people: int, start_date: date, origin: Airport, destination: Airport
) -> List[Connection]:
    """All connections in the week starting on the given date, with exact prices"""
    if destination not in connected_airports(origin):
        return []
    response = make_request(
        "https://www.ryanair.com/api/booking/v4/en-gb/availability",
        parameters=dict(
            ADT=num_people,  # number of adults
            TEEN=0,  # number of 12-15 year olds
            CHD=0,  # number of 2-11 year olds
            INF=0,  # number of <2 year olds
            DateIn="",  # empty for one-way
            DateOut=start_date.isoformat(),
            Origin=origin.iata,
            Destination=destination.iata,
            Disc=0,  # no idea what this is
            promoCode="",
            IncludeConnectingFlights=False,
            FlexDaysBeforeOut=0,
            FlexDaysOut=6,
            ToUs="AGREED",
        ),
    )
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
        for date_info in response["trips"][0]["dates"]
        for flight in date_info["flights"]
        if flight["faresLeft"] == -1 or flight["faresLeft"] >= num_people
    ]
