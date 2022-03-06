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
    def total_price(self):
        return (
            self.home_to_destination.price.in_euro
            + self.destination_to_home.price.in_euro
        )
