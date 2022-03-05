from datetime import timedelta
from functools import cache, cached_property
from typing import Dict, List, Tuple
from dataclasses import dataclass
from urllib import response
from chalicelib.journey import Journey
from chalicelib.scraper.search_parameters import SearchParameters
from chalicelib.timeframe import TimeFrame
from .connection import Connection
from scraper.ryanair import search


@dataclass(frozen=True)
class Request:
    timerange: TimeFrame
    duration_days: Tuple(int, int)  # number of days (min,max)
    origin_cities: List[str]

    @cached_property
    def trip_dates(self) -> List[TimeFrame]:
        dates = []
        for i in range(self.duration_days[0], self.duration_days[1]):
            start = self.timerange.get_startdate()
            end = start + timedelta(days=i)

            while end < self.timerange.get_enddate():
                dates.append(TimeFrame(start=start, end=end))
                start = start + timedelta(days=1)
                end = start + timedelta(days=i)
        return dates

    @cached_property
    def airports(self) -> Dict:
        # call scraper for mapping (city:str,airports:str[])
        None

    @cache
    def city_connections(self, city: str) -> List[Connection]:
        """fetch all possible journeys from 'city:str'"""
        journeys = []
        # for city_from in self.origin_cities:
        for iata_from in self.airports[city]:
            for timeframe in self.tripdates:
                for city_to in self.airports.keys:
                    for iata_to in self.airports[city_to]:
                        par_to = SearchParameters(
                            num_people=len(self.origin_cities),
                            flight_date=timeframe.get_startdate(),
                            origin_iata=iata_from,
                            destination_iata=iata_to,
                        )
                        flights_to = search(par_to)

                        par_from = SearchParameters(
                            num_people=len(self.origin_cities),
                            flight_date=timeframe.get_startdate(),
                            origin_iata=iata_from,
                            destination_iata=iata_to,
                        )
                        flights_from = search(par_from)
                        for towards in flights_to:
                            journeys += [
                                Journey(
                                    start_connection=towards, end_connection=backwards
                                )
                                for backwards in flights_from
                            ]

    def find_overlap(self):
        connections_per_city = {
            city: self.city_connections(city) for city in self.origin_cities
        }

        for i in range(len(self.origin_cities)):
            for j in range(i + 1, len(self.origin_cities)):
                city_i = connections_per_city.keys[i]
                city_j = connections_per_city.keys[j]
                # l = [c for c in connections_per_city[city_i] if [temp.to_airport for temp in connections_per_city[city_j]]
