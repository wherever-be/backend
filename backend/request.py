from dataclasses import dataclass
from datetime import timedelta
from functools import cached_property
from typing import List, Union

from backend.apis import rough_connections, world
from backend.geography import City, Country
from .friend import Friend
from .journey import Journey
from .response import Response
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

    @classmethod
    def from_frontend_json(cls, json):
        return cls(
            time_frame=TimeFrame.from_frontend_json(json["timeFrame"]),
            min_days=json["durationRange"]["min"],
            max_days=json["durationRange"]["max"],
            friends=[
                Friend.from_frontend_json(friend_json)
                for friend_json in json["friends"]
            ],
            destination_country=(
                world().country_by_code(json["destination"]["country"])
                if "country" in json["destination"]
                else None
            ),
            destination_city=(
                world().city_by_code(json["destination"]["city"])
                if "city" in json["destination"]
                else None
            ),
        )

    @cached_property
    def response(self):
        return Response(trips=self.rough_trips)

    @property
    def rough_trips(self) -> List[Trip]:
        return [
            trip
            for trip_dates in self.trip_dates
            for destination in self.destination_cities
            for trip in Trip.combine_journeys(
                destination=destination,
                journeys=[
                    self.rough_journeys(
                        friend=friend,
                        trip_dates=trip_dates,
                        destination=destination,
                    )
                    for friend in self.friends
                ],
            )
        ]

    def rough_journeys(self, friend: Friend, trip_dates: TimeFrame, destination: City):
        return [
            Journey(
                friend=friend,
                home_to_destination=home_to_destination,
                destination_to_home=destination_to_home,
            )
            for home_airport in friend.city.airports
            for destination_airport in destination.airports
            for home_to_destination in rough_connections(
                origin=home_airport,
                destination=destination_airport,
                flight_date=trip_dates.start_date,
            )
            for destination_to_home in rough_connections(
                origin=destination_airport,
                destination=home_airport,
                flight_date=trip_dates.end_date,
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

    @property
    def destination_cities(self):
        if self.destination_city is not None:
            yield self.destination_city
            return
        countries = (
            [self.destination_country]
            if self.destination_country is not None
            else world().countries
        )
        for country in countries:
            for city in country.cities:
                yield city
