from dataclasses import dataclass
from datetime import date, timedelta


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

    def __len__(self):
        return (self.end_date - self.start_date).days + 1

    def __iter__(self):
        current_date = self.start_date
        while True:
            if current_date > self.end_date:
                return
            yield current_date
            current_date = current_date + timedelta(days=1)
