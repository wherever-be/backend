from dataclasses import dataclass
from typing import List

from .trip import Trip


@dataclass(frozen=True)
class Response:
    trips: List[Trip]

    @property
    def frontend_json(self):
        return {"searchResults": [trip.frontend_json for trip in self.trips]}
