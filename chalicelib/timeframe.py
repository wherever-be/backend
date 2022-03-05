from dataclasses import dataclass
from datetime import date
from tracemalloc import start


@dataclass(frozen=True)
class TimeFrame:
    start: date
    end: date

    def get_startdate(self) -> date:
        return self.start

    def get_enddate(self) -> date:
        return self.end
