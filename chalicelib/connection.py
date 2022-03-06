from dataclasses import dataclass
from datetime import datetime

from chalicelib.geography import Airport
from .price import Price


@dataclass(frozen=True)
class Connection:
    from_airport: Airport
    departure: datetime
    to_airport: Airport
    arrival: datetime
    price: Price
