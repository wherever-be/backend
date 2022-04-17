from functools import wraps

from .cache_collection import CacheCollection
from .expiring_cache import ExpiringCache


all_caches = CacheCollection.empty()


def expiring_cache(chunk_size=1024):
    """A thread-safe expiring cache"""

    def decorator(function):
        cache = ExpiringCache.empty(function=function, chunk_size=chunk_size)
        all_caches.add_(cache)

        @wraps(function)
        def decorated(*args, **kwargs):
            return cache.get_(args=args, kwargs=kwargs)

        return decorated

    return decorator
