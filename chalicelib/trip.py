from dataclasses import dataclass
from typing import Generator, List

from chalicelib.geography import City
from .journey import Journey


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
            return
        for other_journeys in cls.combine_journeys(
            destination=destination, journeys=journeys[1:]
        ):
            for journey in journeys[0]:
                yield cls(
                    destination=destination,
                    journeys=[journey] + other_journeys.journeys,
                )