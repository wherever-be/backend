from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class SearchParameters:
    num_people: int
    flight_date: date
    origin_iata: str
    destination_iata: str
