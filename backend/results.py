from dataclasses import dataclass
from typing import List

from .trip import Trip


@dataclass(frozen=True)
class Results:
    trips: List[Trip]

    @property
    def frontend_json(self):
        return {"searchResults": [trip.frontend_json for trip in self.good_trips]}

    @property
    def good_trips(self):
        return sorted(self.trips, key=lambda trip: trip.goodness, reverse=True)
