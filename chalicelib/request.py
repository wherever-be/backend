from dataclasses import dataclass
from datetime import timedelta
from functools import cached_property, lru_cache
from typing import List

from chalicelib.geography import City
from chalicelib.scraper import list_countries, search_flights
from .friend import Friend
from .journey import Journey
from .time_frame import TimeFrame
from .trip import Trip


@dataclass(frozen=True)
class Request:
    time_frame: TimeFrame
    min_days: int
    max_days: int
    friends: List[Friend]

    @cached_property
    def trips(self) -> List[Trip]:
        return [
            Trip.combine_journeys(
                destination=destination,
                journeys=[
                    list(
                        self.journeys(
                            friend=friend,
                            trip_dates=trip_dates,
                            destination=destination,
                        )
                    )
                    for friend in self.friends
                ],
            )
            for trip_dates in self.trip_dates
            for destination in self.destination_cities
        ]

    @lru_cache()
    def journeys(self, friend: Friend, trip_dates: TimeFrame, destination: City):
        return [
            Journey(
                friend=friend,
                home_to_destination=home_to_destination,
                destination_to_home=destination_to_home,
            )
            for home_airport in friend.city.airports
            for destination_airport in destination.airports
            for home_to_destination in search_flights(
                num_people=1,
                flight_date=trip_dates.start_date,
                origin_iata=home_airport.iata,
                destination_iata=destination_airport.iata,
            )
            for destination_to_home in search_flights(
                num_people=1,
                flight_date=trip_dates.end_date,
                origin_iata=destination_airport.iata,
                destination_iata=home_airport.iata,
            )
        ]

    @property
    def trip_dates(self):
        for start_date in self.time_frame:
            for duration_days in range(self.min_days, self.max_days + 1):
                end_date = start_date + timedelta(days=duration_days)
                if end_date > self.time_frame.end_date:
                    break
                yield TimeFrame(
                    start_date=start_date,
                    end_date=end_date,
                )

    def destination_cities(self):
        for country in list_countries():
            for city in country.cities:
                yield city
