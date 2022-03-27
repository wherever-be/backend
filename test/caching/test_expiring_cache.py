from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
import time

from backend.caching import ExpiringCache


def test_save_load():
    def im_slow():
        time.sleep(0.1)

    def measure_time(dummy):
        start_time = time.time()
        cache.get_(args=(), kwargs={})
        return time.time() - start_time

    def test_time(bias):
        total_start_time = time.time()
        with ThreadPoolExecutor(max_workers=4) as executor:
            execution_times = list(executor.map(measure_time, range(8)))

        assert bias < max(execution_times) < bias + 0.1
        assert time.time() - total_start_time < bias + 0.1

    cache = ExpiringCache.empty(function=im_slow, duration=timedelta(minutes=1))
    test_time(0.1)
    cache.save()
    test_time(0.0)
    cache = ExpiringCache.empty(function=im_slow, duration=timedelta(minutes=1))
    cache.load_()
    test_time(0.0)


def test_load_missing():
    def im_slow():
        time.sleep(0.1)

    def measure_time(dummy):
        start_time = time.time()
        cache.get_(args=(), kwargs={})
        return time.time() - start_time

    cache = ExpiringCache.empty(function=im_slow, duration=timedelta(minutes=1))
    cache.path.unlink(missing_ok=True)
    cache.load_()
    total_start_time = time.time()
    with ThreadPoolExecutor(max_workers=4) as executor:
        execution_times = list(executor.map(measure_time, range(8)))

    assert 0.1 < max(execution_times) < 0.2
    assert time.time() - total_start_time < 0.2
