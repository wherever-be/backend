from dataclasses import dataclass

from backend.apis import world
from backend.geography import City


@dataclass(frozen=True)
class Friend:
    name: str
    city: City

    @classmethod
    def from_frontend_json(cls, json):
        return cls(name=json["name"], city=world().city_by_code(json["city"]))
