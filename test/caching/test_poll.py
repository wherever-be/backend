from time import time

from backend.apis import world
from backend.caching.poll import poll_single


def test_rate_limit():
    olsztyn = world().city_by_code("OLSZTYN")
    brno = world().city_by_code("BRNO")
    # run once to make cache
    poll_single(from_city=olsztyn, to_city=brno)
    # run again to start cooldown afresh
    poll_single(from_city=olsztyn, to_city=brno)

    start_time = time()
    poll_single(from_city=olsztyn, to_city=brno)
    assert time() - start_time > 0.4
