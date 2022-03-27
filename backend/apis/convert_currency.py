from datetime import timedelta
import requests
import json

from backend.caching import expiring_cache


def convert_currency(amount: float, from_currency: str, to_currency: str):
    return amount * _pln_rates()[from_currency] / _pln_rates()[to_currency]


@expiring_cache(duration=timedelta(hours=1))
def _pln_rates():
    return {
        "PLN": 1,
        **{
            info["code"]: info["mid"]
            for table in ["a", "b"]
            for info in _get_table(table)
        },
    }


def _get_table(table: str):
    return json.loads(
        requests.get(
            f"http://api.nbp.pl/api/exchangerates/tables/{table}",
            params=dict(format="json"),
        ).text
    )[0]["rates"]
