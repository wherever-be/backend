from datetime import date, timedelta
from itertools import combinations
import random
from ratelimit import limits, sleep_and_retry
from tqdm import tqdm
from threading import Thread

from backend.apis import world
from backend.caching import all_caches
from backend.friend import Friend
from backend.query import Query
from backend.search import search
from backend.time_frame import TimeFrame


def background_poll_loop():
    thread = Thread(target=poll_loop, name="polling", daemon=True)
    thread.start()
    return thread


def poll_loop():
    all_caches.load_all()
    while True:
        poll_all()
        all_caches.clean_all()
        all_caches.save_all()


@sleep_and_retry
@limits(calls=1, period=60 * 60)
def poll_all():
    cities = list(world().cities)
    city_pairs = list(combinations(cities, 2))
    loading_bar = tqdm(city_pairs, desc="Refreshing cache", smoothing=0)
    for from_city, to_city in loading_bar:
        loading_bar.set_postfix_str(f"{from_city.name} => {to_city.name}")
        poll_single(from_city=from_city, to_city=to_city)


@sleep_and_retry
@limits(calls=1, period=0.25)
def poll_single(from_city, to_city):
    start_date = date.today() + timedelta(days=2 ** random.randint(0, 4))
    end_date = start_date + timedelta(days=2 ** random.randint(3, 8))
    min_days = random.randint(2, 5)
    max_days = min_days + random.randint(1, 10)
    query = Query(
        time_frame=TimeFrame(start_date=start_date, end_date=end_date),
        min_days=min_days,
        max_days=max_days,
        friends=[Friend(name="CACHE REFRESH", city=from_city)],
        destination_country=next(
            country for country in world().countries if to_city in country.cities
        ),
        destination_city=to_city,
    )
    search(query)
