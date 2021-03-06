from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from threading import Lock
from typing import Any, Callable, Dict

from .dict_io import save_dict, load_dict


@dataclass(frozen=False)
class ExpiringCache:
    function: Callable
    _dict: Dict[Any, "Entry"]
    lock: Lock
    chunk_size: int

    @property
    def path(self):
        import backend

        cache_path = Path(backend.__file__).parent.parent / "cache"
        return cache_path / f"{self.function.__module__}:{self.function.__name__}"

    @classmethod
    def empty(cls, function: Callable, chunk_size: int):
        return cls(
            function=function,
            _dict={},
            lock=Lock(),
            chunk_size=chunk_size,
        )

    @classmethod
    @contextmanager
    def duration(cls, duration: timedelta):
        old_duration = cache_duration.get()
        cache_duration.set(duration)
        yield
        cache_duration.set(old_duration)

    def get_(self, args, kwargs):
        encoded_args = self.encode_args(args=args, kwargs=kwargs)
        with self.lock:
            if encoded_args not in self._dict:
                self._dict[encoded_args] = ExpiringCache.Entry.empty()
            entry = self._dict[encoded_args]
        with entry.lock:
            if entry.is_valid:
                return entry.contents
            result = self.function(*args, **kwargs)
        self.set_(args=args, kwargs=kwargs, value=result)
        return result

    def set_(self, args, kwargs, value):
        encoded_args = self.encode_args(args=args, kwargs=kwargs)
        with self.lock:
            self._dict[encoded_args].update_(value)

    def load_(self):
        with self.lock:
            if not self.path.exists():
                return
            data = load_dict(self.path)
            self._dict = {
                key: entry
                for key, datum in data.items()
                if (
                    entry := self.Entry(
                        lock=Lock(),
                        last_updated=datum["last_updated"],
                        contents=datum["contents"],
                        populated=True,
                    )
                ).is_valid
            }

    def save(self):
        with self.lock:
            as_dict = {}
            for key, entry in self._dict.items():
                with entry.lock:
                    if not entry.populated:
                        continue
                    as_dict[key] = dict(
                        last_updated=entry.last_updated, contents=entry.contents
                    )
            save_dict(as_dict, path=self.path, chunk_size=self.chunk_size)

    def clean_(self):
        """Remove outdated entries"""
        with self.lock:
            self._dict = {
                key: entry for key, entry in self._dict.items() if entry.is_valid
            }

    @staticmethod
    def encode_args(args, kwargs):
        return (args, tuple(kwargs.items()))

    @dataclass(frozen=False)
    class Entry:
        lock: Lock
        last_updated: datetime
        contents: Any
        populated: bool

        @property
        def is_valid(self):
            if self.populated:
                if cache_duration.get() is None:
                    return True
                if datetime.now() < self.last_updated + cache_duration.get():
                    return True
            return False

        @classmethod
        def empty(cls):
            return cls(
                lock=Lock(), last_updated=datetime.now(), contents=None, populated=False
            )

        def update_(self, contents):
            self.last_updated = datetime.now()
            self.contents = contents
            self.populated = True


cache_duration: ContextVar[timedelta] = ContextVar("cache_duration", default=None)
