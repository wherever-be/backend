from datetime import date, datetime
from ratelimit import limits, sleep_and_retry
from typing import List

from backend.caching import expiring_cache
from backend.connection import Connection
from backend.geography import Airport
from backend.price import Price
from .connected_airports import connected_airports
from .errors import RyanairAPIError, RyanairBlacklistError
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


@expiring_cache()
def _precise_connections(
    num_people: int, start_date: date, origin: Airport, destination: Airport
):
    """All connections in the week starting on the given date, with exact prices"""
    if destination not in connected_airports(origin):
        return []
    try:
        response = _make_request(
            num_people=num_people,
            start_date_iso=start_date.isoformat(),
            origin_iata=origin.iata,
            destination_iata=destination.iata,
        )
    except RyanairAPIError as api_error:
        if api_error.code == 404:
            if ryanair_blacklist():
                raise RyanairBlacklistError()
            return []  # no connecting flights
        raise api_error
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


def ryanair_blacklist():
    """Have we been blacklisted by Ryanair?"""
    try:
        _make_request(
            num_people=1,
            start_date_iso=date.today().isoformat(),
            origin_iata="KRK",
            destination_iata="EIN",
        )
    except RyanairAPIError as api_error:
        if api_error.code == 404:
            return True
        raise api_error
    return False


@sleep_and_retry
@limits(calls=1, period=0.25)
def _make_request(
    num_people: int, start_date_iso: str, origin_iata: str, destination_iata: str
):
    return make_request(
        "https://www.ryanair.com/api/booking/v4/en-gb/availability",
        parameters=dict(
            ADT=num_people,  # number of adults
            TEEN=0,  # number of 12-15 year olds
            CHD=0,  # number of 2-11 year olds
            INF=0,  # number of <2 year olds
            DateIn="",  # empty for one-way
            DateOut=start_date_iso,
            Origin=origin_iata,
            Destination=destination_iata,
            Disc=0,  # no idea what this is
            promoCode="",
            IncludeConnectingFlights=False,
            FlexDaysBeforeOut=0,
            FlexDaysOut=6,
            ToUs="AGREED",
        ),
    )
