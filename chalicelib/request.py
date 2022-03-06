from dataclasses import dataclass
from datetime import timedelta
from functools import cached_property
from typing import List, Union

from chalicelib.geography import City, Country
from chalicelib.scraper import list_countries, rough_connection
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
    destination_country: Union[Country, None]
    destination_city: Union[City, None]

    @cached_property
    def rough_trips(self) -> List[Trip]:
        return [
            Trip.combine_journeys(
                destination=destination,
                journeys=[
                    self.journeys(
                        friend=friend,
                        trip_dates=trip_dates,
                        destination=destination,
                    )
                    for friend in self.friends
                ],
            )
            for trip_dates in self.trip_dates
            for destination in self.destination_cities
        ]

    def rough_journeys(self, friend: Friend, trip_dates: TimeFrame, destination: City):
        return [
            Journey(
                friend=friend,
                home_to_destination=rough_connection(
                    origin=home_airport,
                    destination=destination_airport,
                    flight_date=trip_dates.start_date,
                ),
                destination_to_home=rough_connection(
                    origin=destination_airport,
                    destination=home_airport,
                    flight_date=trip_dates.end_date,
                ),
            )
            for home_airport in friend.city.airports
            for destination_airport in destination.airports
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
        if self.destination_city is not None:
            yield self.destination_city
            return
        countries = (
            [self.destination_country]
            if self.destination_country is not None
            else list_countries()
        )
        for country in countries:
            for city in country.cities:
                yield city
