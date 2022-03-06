from dataclasses import dataclass
from typing import List

from .airport import Airport
from .city import City
from .country import Country


@dataclass(frozen=True)
class World:
    countries: List[Country]

    def country_by_code(self, code: str):
        return next(country for country in self.countries if country.code == code)

    def city_by_code(self, code: str):
        return next(
            city
            for country in self.countries
            for city in country.cities
            if city.code == code
        )

    def airport_by_iata(self, iata: str):
        return next(
            airport
            for country in self.countries
            for city in country.cities
            for airport in city.airports
            if airport.iata == iata
        )
