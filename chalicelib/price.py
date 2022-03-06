from dataclasses import dataclass

from chalicelib.scraper import eur_rate


@dataclass(frozen=True)
class Price:
    amount: float
    currency: str

    @property
    def in_euro(self) -> "Price":
        if self.currency == "EUR":
            return self
        return Price(amount=self.amount / eur_rate(self.currency), currency="EUR")

    @property
    def frontend_json(self):
        in_euro = self.in_euro
        return {"amount": in_euro.amount, "currency": in_euro.currency}

    def __add__(self, other: "Price") -> "Price":
        assert self.currency == other.currency
        return Price(amount=self.amount + other.amount, currency=self.currency)
