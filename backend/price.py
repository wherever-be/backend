from dataclasses import dataclass

from backend.apis import convert_currency


@dataclass(frozen=True)
class Price:
    amount: float
    currency: str

    def to_currency(self, currency: str) -> "Price":
        if self.currency == currency:
            return self
        return Price(
            amount=convert_currency(
                self.amount, from_currency=self.currency, to_currency=currency
            ),
            currency=currency,
        )

    @property
    def frontend_json(self):
        in_euro = self.to_currency("EUR")
        return {"amount": in_euro.amount, "currency": in_euro.currency}

    def __add__(self, other: "Price") -> "Price":
        assert self.currency == other.currency
        return Price(amount=self.amount + other.amount, currency=self.currency)
