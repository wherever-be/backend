import requests
import re

from .make_request import make_request
from backend.geography import World, Country, City, Airport


def world() -> World:

    q = str(requests.get("https://wizzair.com/buildnumber").content)
    wizzair_api = (
        "https://be.wizzair.com/"
        + re.search("[0-9]+[.][0-9]+[.][0-9]+", q)
        + "Api/asset/map?languageCode=en-gb"
    )

    response = requests.get(wizzair_api, params="").json()

    countries = {
        (city["countryCode"], city["countryName"]): [] for city in response["cities"]
    }
    for city in response["cities"]:
        countries[(city["countryCode"], city["countryName"])].append(
            City(
                name=city["shortName"],
                code="no_city_code",
                airports=[Airport(name=city["shortName"], iata=city["iata"])],
            )
        )

    return World(
        countries=[
            Country(name=country, code=code, cities=countries[country])
            for code, country in countries
        ]
    )
