"""Thread-safe client-side rate limiter for the QrMaint API.

Enforces all four official rate-limit windows simultaneously:
- 10 requests per second
- 9 000 requests per 15 minutes
- 45 000 requests per 12 hours
- 1 000 000 requests per 7 days
"""

import threading
import time

from limits import parse
from limits.storage import MemoryStorage
from limits.strategies import MovingWindowRateLimiter


class RateLimiter:
    """Blocking rate limiter that respects the QrMaint API quotas.

    Uses a moving-window strategy (``limits`` library) backed by in-process
    memory.  All four official windows are checked atomically under a
    ``threading.Lock`` so that multi-threaded callers cannot race between the
    ``test`` and ``hit`` calls.

    Usage::

        limiter = RateLimiter()
        limiter.acquire()   # blocks until a request slot is available
        # ... make the HTTP request ...
    """

    _WINDOWS = [
        "10 per 1 second",
        "9000 per 15 minutes",
        "45000 per 12 hours",
        "1000000 per 7 days",
    ]
    _KEY = "qrmaint"

    def __init__(self) -> None:
        """Initialize in-memory storage and parse all rate-limit windows."""
        self._storage = MemoryStorage()
        self._strategy = MovingWindowRateLimiter(self._storage)
        self._limits = [parse(w) for w in self._WINDOWS]
        self._lock = threading.Lock()

    def acquire(self) -> None:
        """Block the calling thread until all rate-limit windows allow a request.

        Checks every window atomically.  If any window is exhausted the method
        sleeps for 50 ms and retries, repeating until all windows permit the
        request and the counters have been incremented.
        """
        while True:
            with self._lock:
                if all(self._strategy.test(lim, self._KEY) for lim in self._limits):
                    for lim in self._limits:
                        self._strategy.hit(lim, self._KEY)
                    return
            time.sleep(0.05)
