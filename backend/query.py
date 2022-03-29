from dataclasses import dataclass
from datetime import timedelta
from typing import List, Union

from backend.apis import world
from backend.geography import City, Country
from .friend import Friend
from .time_frame import TimeFrame


@dataclass(frozen=True)
class Query:
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

    @property
    def max_trips(self):
        return min(64, 32 + sum(1 for city in self.destination_cities))

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
