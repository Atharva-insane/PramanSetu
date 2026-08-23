import time
from collections import defaultdict
from typing import Dict, List, Tuple
from fastapi import Request, HTTPException


class InMemoryRateLimiter:
    """
    Sliding-window in-memory rate limiter for resource-intensive and sensitive endpoints.
    Protects AI image inference, database transactions, and public verification endpoints.
    """
    def __init__(self):
        # Maps (identifier, endpoint_tag) -> list of request timestamps
        self._history: Dict[Tuple[str, str], List[float]] = defaultdict(list)

    def is_allowed(self, identifier: str, tag: str, limit_per_minute: int) -> Tuple[bool, int]:
        """
        Evaluates whether the client request is permitted under the sliding window limit.
        Returns (is_permitted, retry_after_seconds).
        """
        now = time.time()
        window_start = now - 60.0

        key = (identifier, tag)
        # Purge timestamps outside current 60s window
        timestamps = [ts for ts in self._history[key] if ts > window_start]
        self._history[key] = timestamps

        if len(timestamps) >= limit_per_minute:
            oldest_ts = timestamps[0]
            retry_after = max(1, int(60.0 - (now - oldest_ts)))
            return False, retry_after

        self._history[key].append(now)
        return True, 0

    def check_rate_limit(self, request: Request, tag: str, limit_per_minute: int):
        """
        FastAPI dependency helper to enforce rate limiting and raise HTTP 429 on exhaustion.
        """
        client_ip = request.client.host if request.client else "127.0.0.1"
        # Combine IP and authorization header if present for per-user throttling
        auth_header = request.headers.get("Authorization", "")
        identifier = f"{client_ip}:{hash(auth_header) if auth_header else 'anon'}"

        allowed, retry_after = self.is_allowed(identifier, tag, limit_per_minute)
        if not allowed:
            raise HTTPException(
                status_code=429,
                detail={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests to endpoint '{tag}'. Please retry after {retry_after} seconds.",
                    "retry_after_seconds": retry_after
                },
                headers={"Retry-After": str(retry_after)}
            )


# Global rate limiter instance
global_rate_limiter = InMemoryRateLimiter()
