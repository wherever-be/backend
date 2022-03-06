from cachetools import cached, TTLCache
from typing import List

from chalicelib.geography import Country, City, Airport
from .ryanair import make_request


@cached(cache=TTLCache(maxsize=1, ttl=24 * 60 * 60))
def list_countries() -> List[Country]:
    response = make_request(
        "https://www.ryanair.com/api/locate/v1/autocomplete/airports",
        parameters=dict(phrase="", market="en-gb"),
    )
    return [
        Country(
            name=country_name,
            code=country_code,
            cities=[
                City(
                    name=city_name,
                    code=city_code,
                    airports=[
                        Airport(
                            name=airport["name"],
                            iata=airport["code"],
                        )
                        for airport in response
                        if airport["city"]["code"] == city_code
                    ],
                )
                for city_name, city_code in {
                    (airport["city"]["name"], airport["city"]["code"])
                    for airport in response
                    if airport["country"]["code"] == country_code
                }
            ],
        )
        for country_name, country_code in {
            (airport["country"]["name"], airport["country"]["code"])
            for airport in response
        }
    ]
