from dataclasses import dataclass
from functools import cached_property, reduce
from typing import Generator, List

from backend.geography import City
from .journey import Journey
from .time_frame import TimeFrame


@dataclass(frozen=True)
class Trip:
    """The trip of an entire group of friends"""

    destination: City
    journeys: List[Journey]

    @classmethod
    def combine_journeys(
        cls, destination: City, journeys: List[List[Journey]]
    ) -> Generator["Trip", None, None]:
        if len(journeys) == 0:
            yield cls(destination=destination, journeys=[])
            return
        for other_journeys in cls.combine_journeys(
            destination=destination, journeys=journeys[1:]
        ):
            for journey in journeys[0]:
                yield cls(
                    destination=destination,
                    journeys=[journey] + other_journeys.journeys,
                )

    @property
    def frontend_json(self):
        return {
            "id": id(self),
            "destination": self.destination.code,
            "goodness": self.goodness,
            "journeys": [journey.frontend_json for journey in self.journeys],
        }

    @cached_property
    def time_frame(self):
        return TimeFrame(
            start_date=min(
                journey.home_to_destination.departure.date()
                for journey in self.journeys
            ),
            end_date=max(
                journey.destination_to_home.arrival.date() for journey in self.journeys
            ),
        )

    @cached_property
    def goodness(self):
        return -self.total_price.amount / len(self.journeys)

    def similarity(self, other: "Trip"):
        """A score used to make results diverse"""
        destination_similarity = 8 if self.destination == other.destination else 0
        date_similarity = (
            -abs((self.time_frame.start_date - other.time_frame.start_date).days) * 0.25
        )
        duration_similarity = -abs(len(self.time_frame) - len(other.time_frame)) * 2
        return destination_similarity + date_similarity + duration_similarity

    @cached_property
    def total_price(self):
        return reduce(
            lambda a, b: a + b, (journey.total_price for journey in self.journeys)
        )
