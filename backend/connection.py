from dataclasses import dataclass
from datetime import datetime

from backend.geography import Airport
from .price import Price


@dataclass(frozen=True)
class Connection:
    from_airport: Airport
    departure: datetime
    to_airport: Airport
    arrival: datetime
    price: Price

    @property
    def frontend_json(self):
        return {
            "departure": {
                "date": self.departure.isoformat(),
                "port": self.from_airport.iata,
            },
            "arrival": {
                "date": self.arrival.isoformat(),
                "port": self.to_airport.iata,
            },
            "price": self.price.frontend_json,
            "bookingLink": f"https://www.ryanair.com/lv/en/trip/flights/select?adults=1&teens=0&children=0&infants=0&dateOut={self.departure.date().isoformat()}&dateIn=&isConnectedFlight=false&isReturn=false&discount=0&promoCode=&originIata={self.from_airport.iata}&destinationIata={self.to_airport.iata}",
        }
