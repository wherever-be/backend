from typing import List

from backend.caching import expiring_cache
from backend.geography import Airport
from .world import world
from .make_request import make_request


@expiring_cache()
def connected_airports(origin: Airport) -> List[Airport]:
    response = make_request(
        "https://www.ryanair.com/api/locate/v1/autocomplete/routes",
        parameters=dict(arrivalPhrase="", departurePhrase=origin.iata),
    )
    return [
        world().airport_by_iata(route["arrivalAirport"]["code"]) for route in response
    ]
