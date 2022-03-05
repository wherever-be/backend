from dataclasses import dataclass
from typing import List

from .city import City


@dataclass(frozen=True)
class Country:
    name: str
    code: str
    cities: List[City]
