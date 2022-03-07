from dataclasses import dataclass


@dataclass(frozen=True)
class Airport:
    name: str
    iata: str
