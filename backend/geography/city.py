from dataclasses import dataclass
from typing import List

from .airport import Airport


@dataclass(frozen=True)
class City:
    name: str
    code: str
    airports: List[Airport]
