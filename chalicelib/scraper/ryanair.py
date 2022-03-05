import requests
from typing import List
from datetime import datetime

from chalicelib.connection import Connection
from chalicelib.price import Price
from .errors import AirportsNotConnectedError, TooManyRequestsError, UnknownError
from .search_parameters import SearchParameters


def search(search_parameters: SearchParameters) -> List[Connection]:
    try:
        response = make_request(search_parameters)
    except AirportsNotConnectedError:
        return []
    flights = response["trips"][0]["dates"][0]["flights"]
    return [
        Connection(
            from_airport=search_parameters.origin_iata,
            departure=datetime.fromisoformat(flight["segments"][0]["time"][0]),
            to_airport=search_parameters.destination_iata,
            arrival=datetime.fromisoformat(flight["segments"][-1]["time"][-1]),
            price=Price(
                amount=flight["regularFare"]["fares"][0]["amount"],
                currency=response["currency"],
            ),
        )
        for flight in flights
    ]


# TODO: retry on some errors, throttle
def make_request(search_parameters: SearchParameters):
    request = requests.get(
        "https://www.ryanair.com/api/booking/v4/en-gb/availability",
        params=dict(
            ADT=search_parameters.num_people,  # number of adults
            TEEN=0,  # number of 12-15 year olds
            CHD=0,  # number of 2-11 year olds
            INF=0,  # number of <2 year olds
            DateIn="",  # empty for one-way
            DateOut=search_parameters.flight_date.isoformat(),
            Origin=search_parameters.origin_iata,
            Destination=search_parameters.destination_iata,
            Disc=0,  # no idea what this is
            promoCode="",
            IncludeConnectingFlights=False,
            FlexDaysBeforeOut=0,
            FlexDaysOut=0,  # TODO: this can be up to 6, then we get results for later dates as well
            ToUs="AGREED",
        ),
    )
    if request.status_code == 429:
        raise TooManyRequestsError()
    if request.status_code == 404:
        raise AirportsNotConnectedError()
    if request.status_code != 200:
        raise UnknownError()
    return request.json()
