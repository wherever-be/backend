from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import wraps
from threading import Lock
from typing import Any, Dict


def expiring_cache(duration: timedelta):
    """A thread-safe expiring cache"""
    cache_lock = Lock()
    cache: Dict[Any, ExpiringCacheEntry] = {}

    def decorator(function):
        @wraps(function)
        def decorated(*args, **kwargs):
            encoded_args = (args, tuple(kwargs.items()))
            with cache_lock:
                if encoded_args not in cache:
                    cache[encoded_args] = ExpiringCacheEntry.empty()
                entry = cache[encoded_args]
            with entry.lock:
                if entry.populated:
                    if datetime.now() < entry.last_updated + duration:
                        return entry.contents
                result = function(*args, **kwargs)
            with cache_lock:
                cache[encoded_args].update_(result)
            return result

        return decorated

    return decorator


@dataclass(frozen=False)
class ExpiringCacheEntry:
    lock: Lock
    last_updated: datetime
    contents: Any
    populated: bool

    @classmethod
    def empty(cls):
        return cls(
            lock=Lock(), last_updated=datetime.now(), contents=None, populated=False
        )

    def update_(self, contents):
        self.last_updated = datetime.now()
        self.contents = contents
        self.populated = True
