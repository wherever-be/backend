from dataclasses import dataclass


@dataclass(frozen=True)
class Price:
    amount: float
    currency: str

    def to_currency(self, currency: str) -> "Price":
        pass  # TODO
