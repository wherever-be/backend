from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class TimeFrame:
    start_date: date
    end_date: date
