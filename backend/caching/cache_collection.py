from dataclasses import dataclass
from threading import Lock
from typing import List

from .expiring_cache import ExpiringCache


@dataclass(frozen=False)
class CacheCollection:
    lock: Lock
    caches: List[ExpiringCache]

    @classmethod
    def empty(cls):
        return cls(lock=Lock(), caches=[])

    def add_(self, cache: ExpiringCache):
        self.caches.append(cache)

    def load_all(self):
        with self.lock:
            for cache in self.caches:
                cache.load_()

    def save_all(self):
        with self.lock:
            for cache in self.caches:
                cache.save()

    def clean_all(self):
        with self.lock:
            for cache in self.caches:
                cache.clean_()
