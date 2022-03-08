from datetime import date, datetime, timedelta
from typing import Dict, List

from backend.connection import Connection
from backend.expiring_cache import expiring_cache
from backend.geography import Airport
from backend.price import Price
from .ryanair import make_request


def rough_connections(
    origin: Airport, destination: Airport, flight_date: date
) -> List[Connection]:
    """
    Quickly get the cheapest connections on the given day.
    Prices are sometimes a bit lower than actual.
    """
    try:
        return [
            _rough_connections_dict(origin=origin, destination=destination)[flight_date]
        ]
    except KeyError:
        return []


@expiring_cache(duration=timedelta(hours=12))
def _rough_connections_dict(
    origin: Airport, destination: Airport
) -> Dict[date, Connection]:
    """
    Quickly get the cheapest connections per day for one year into the future.
    Prices are sometimes a bit lower than actual.
    """
    response = make_request(
        f"https://www.ryanair.com/api/farfnd/v4/oneWayFares/{origin.iata}/{destination.iata}/cheapestPerDay",
        parameters=dict(
            outboundDateFrom=date.today().isoformat(),
            outboundDateTo=(date.today() + timedelta(days=356)).isoformat(),
        ),
    )
    return {
        date.fromisoformat(fare["day"]): Connection(
            from_airport=origin,
            departure=datetime.fromisoformat(fare["departureDate"]),
            to_airport=destination,
            arrival=datetime.fromisoformat(fare["arrivalDate"]),
            price=Price(
                amount=fare["price"]["value"],
                currency=fare["price"]["currencyCode"],
            ),
        )
        for fare in response["outbound"]["fares"]
        if not fare["unavailable"]
    }
