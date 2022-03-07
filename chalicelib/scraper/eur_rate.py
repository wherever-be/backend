from bs4 import BeautifulSoup
from cachetools import cached, TTLCache
import requests


def eur_rate(currency: str):
    return _eur_rates()[currency]


@cached(cache=TTLCache(maxsize=1, ttl=1 * 60 * 60))
def _eur_rates():
    request = requests.get(
        "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
    )
    soup = BeautifulSoup(request.text, features="lxml")
    return {
        cube.attrs["currency"]: float(cube.attrs["rate"])
        for cube in soup.find_all("cube")
        if "currency" in cube.attrs
    }
