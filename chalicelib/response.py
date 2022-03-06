from dataclasses import dataclass
from typing import List

from .trip import Trip


@dataclass(frozen=True)
class Response:
    trips: List[Trip]

    @property
    def for_frontend(self):
        return {"searchResults": [trip.for_frontend for trip in self.trips]}
