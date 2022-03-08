from bs4 import BeautifulSoup
from datetime import timedelta
import requests

from backend.expiring_cache import expiring_cache


def eur_rate(currency: str):
    return _eur_rates()[currency]


@expiring_cache(duration=timedelta(hours=1))
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
