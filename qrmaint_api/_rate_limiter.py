"""Thread-safe client-side rate limiter for the QrMaint API.

Enforces the per-second window (10 req/s) using a sliding-window deque.
Longer windows (15 min, 12 h, 7 days) are not enforced client-side because
the sync task never comes close to those thresholds in practice.
"""
from __future__ import annotations

import threading
import time
from collections import deque


class RateLimiter:
    """Blocking rate limiter — 10 requests per second, sliding window.

    Usage::

        limiter = RateLimiter()
        limiter.acquire()   # blocks until a request slot is available
        # ... make the HTTP request ...
    """

    _MAX_PER_SECOND = 10

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._timestamps: deque[float] = deque()

    def acquire(self) -> None:
        """Block until the per-second window allows one more request."""
        while True:
            with self._lock:
                now = time.monotonic()
                while self._timestamps and now - self._timestamps[0] >= 1.0:
                    self._timestamps.popleft()
                if len(self._timestamps) < self._MAX_PER_SECOND:
                    self._timestamps.append(now)
                    return
                wait = 1.0 - (now - self._timestamps[0])
            if wait > 0:
                time.sleep(wait)
