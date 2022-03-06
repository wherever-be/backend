from dataclasses import dataclass

from .connection import Connection
from .friend import Friend


@dataclass(frozen=True)
class Journey:
    """A single person's travels to and from the destination"""

    friend: Friend
    home_to_destination: Connection
    destination_to_home: Connection
