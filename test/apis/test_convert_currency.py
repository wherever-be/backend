from backend.apis import convert_currency


def test_usd_to_pln():
    assert convert_currency(1, from_currency="USD", to_currency="PLN") > 3


def test_pln_to_usd():
    assert convert_currency(1, from_currency="PLN", to_currency="USD") < 0.3


def test_inr_to_mad():
    assert convert_currency(1, from_currency="INR", to_currency="MAD") < 0.5
