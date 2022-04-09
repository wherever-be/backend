from datetime import date, datetime, timedelta
from ratelimit import limits, sleep_and_retry
from typing import Dict, List
import requests
import re

from backend.caching import expiring_cache
from backend.apis.wizzair.errors import WizzairAPIError
from backend.geography import Airport
from backend.connection import Connection


def cheap_connections(
    num_people: int, flight_date: date, origin: Airport, destination: Airport
) -> Dict[date, Connection]:
    None


@expiring_cache(duration=timedelta(hours=12))
def _cheap_connections(
    num_people: int, origin: Airport, destination: Airport
) -> Dict[date, Connection]:

    q = str(requests.get("https://wizzair.com/buildnumber").content)
    wizzair_api = (
        "https://be.wizzair.com/"
        + re.search("[0-9]+[.][0-9]+[.][0-9]+", q)
        + "Api/search/timetable"
    )

    connections = {}
    for i in range(365 // 40):
        response = requests.post(
            wizzair_api,
            json={
                "flightList": [
                    {
                        "departureStation": origin.iata,
                        "arrivalStation": destination.iata,
                        "from": (datetime.today() + timedelta(days=40 * i)).isoformat(),
                        "to": (
                            datetime.today() + timedelta(days=40 * (i + 1))
                        ).isoformat(),
                    },
                ],
                "priceType": "regular",
                "adultCount": 1,
                "childCount": 0,
                "infantCount": 0,
            },
        )
        if response.status_code != 200:
            raise WizzairAPIError(response=response)

        connections_over_month = response.json()["outboundFlights"]

        connections.update(
            {
                datetime.fromisoformat(connection["departureDates"][0]): Connection(
                    from_airport=origin,
                    departure=datetime.fromisoformat(connection["departureDates"][0]),
                    to_airport=destination,
                    price=connection["price"],
                    arrival=datetime.fromisoformat(
                        connection["departureDates"][0]
                    ),  # no arrival time available through API
                )
                for connection in connections_over_month
            }
        )
    return connections


if __name__ == "__main__":
    # returns all flights specified in flightList using start date and dayInterval (e.g. 7 days), use q1.json()['outboundFlights'] or q1.json()['returnFlights']

    q = str(requests.get("https://wizzair.com/buildnumber").content)
    wizzair_api = (
        "https://wizzair.com/"
        + re.search("[0-9]+[.][0-9]+[.][0-9]+", q)
        + "Api/asset/farechart"
    )

    q2 = requests.post(
        wizzair_api,
        json={
            "isRescueFare": False,
            "adultCount": 1,
            "childCount": 0,
            "dayInterval": 3,  # must be greater or equal to 3
            "wdc": False,
            "isFlightChange": False,
            "flightList": [
                {
                    "departureStation": "KFZ",
                    "arrivalStation": "VIE",
                    "date": "2022-07-15",
                },
                {
                    "departureStation": "VIE",
                    "arrivalStation": "KFZ",
                    "date": "2022-09-04",
                },
            ],
        },
    )

    # returns all flights between startdate and enddate specified in flightList, use q1.json()['outboundFlights'] or q1.json()['returnFlights']
    q = str(requests.get("https://wizzair.com/buildnumber").content)
    wizzair_api = (
        "https://be.wizzair.com/"
        + re.search("[0-9]+[.][0-9]+[.][0-9]+", q).group()
        + "/Api/search/timetable"
    )

    q1 = requests.post(
        # "https://be.wizzair.com/12.5.0/Api/search/timetable",
        wizzair_api,
        json={
            "flightList": [
                {
                    "departureStation": "KFZ",
                    "arrivalStation": "VIE",
                    "from": "2022-06-27",
                    "to": "2022-07-31",
                },
                {
                    "departureStation": "VIE",
                    "arrivalStation": "KFZ",
                    "from": (datetime.now() + timedelta(days=40 * 8))
                    .date()
                    .isoformat(),
                    "to": (datetime.now() + timedelta(days=40 * 9)).date().isoformat(),
                },
            ],
            "priceType": "regular",
            "adultCount": 1,
            "childCount": 0,
            "infantCount": 0,
        },
    )

    # returns the flight details (hour, price) on a specific date but looks like it's not directly accesible (Error 451)
    q3 = requests.post(
        "https://be.wizzair.com/12.4.1/Api/search/search",
        json={
            "isFlightChange": False,
            "flightList": [
                {
                    "departureStation": "KFZ",
                    "arrivalStation": "VIE",
                    "departureDate": "2022-08-04",
                },
                {
                    "departureStation": "VIE",
                    "arrivalStation": "KFZ",
                    "departureDate": "2022-08-18",
                },
            ],
            "adultCount": 1,
            "childCount": 0,
            "infantCount": 0,
            "wdc": True,
        },
    )
