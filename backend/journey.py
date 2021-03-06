from dataclasses import dataclass

from .connection import Connection
from .friend import Friend


@dataclass(frozen=True)
class Journey:
    """A single person's travels to and from the destination"""

    friend: Friend
    home_to_destination: Connection
    destination_to_home: Connection

    @property
    def frontend_json(self):
        return {
            "friendName": self.friend.name,
            "staysHome": False,  # TODO: consider staying home
            "homeToDest": self.home_to_destination.frontend_json,
            "destToHome": self.destination_to_home.frontend_json,
        }

    @property
    def total_price(self):
        return self.home_to_destination.price.to_currency(
            "EUR"
        ) + self.destination_to_home.price.to_currency("EUR")
