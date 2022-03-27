from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
import time

from backend.caching import expiring_cache


def test_instant_retrieval():
    @expiring_cache(duration=timedelta(minutes=1))
    def im_slow():
        time.sleep(0.1)

    def measure_time(dummy):
        start_time = time.time()
        im_slow()
        return time.time() - start_time

    total_start_time = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        execution_times = list(executor.map(measure_time, range(8)))

    assert 0.1 < max(execution_times) < 0.2
    assert time.time() - total_start_time < 0.2


def test_retrieved_item():
    @expiring_cache(duration=timedelta(minutes=1))
    def cached(number):
        return number

    def check_correctness(number):
        return cached(number % 3) == number % 3

    with ThreadPoolExecutor(max_workers=4) as executor:
        correctness = list(executor.map(check_correctness, range(8)))

    assert all(correctness)


def test_expiry():
    @expiring_cache(duration=timedelta(seconds=0.05))
    def im_slow(dummy):
        time.sleep(0.1)

    start_time = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        list(executor.map(im_slow, range(4)))
    assert 0.1 < time.time() - start_time < 0.2

    time.sleep(0.1)
    new_start_time = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        list(executor.map(im_slow, range(4)))
    assert 0.1 < time.time() - new_start_time < 0.2
