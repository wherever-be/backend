from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class TimeFrame:
    start_date: date
    end_date: date

    @classmethod
    def from_frontend_json(cls, json):
        return cls(
            start_date=date.fromisoformat(json["start"]),
            end_date=date.fromisoformat(json["end"]),
        )
