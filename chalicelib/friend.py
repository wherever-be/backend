from dataclasses import dataclass

from chalicelib.geography import City


@dataclass(frozen=True)
class Friend:
    name: str
    city: City
