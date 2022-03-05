from dataclasses import dataclass
from datetime import datetime

from .price import Price


@dataclass(frozen=True)
class Connection:
    from_airport: str
    departure: datetime
    to_airport: str
    arrival: datetime
    price: Price
