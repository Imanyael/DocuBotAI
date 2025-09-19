"""
Rate limiting utilities for DocuBotAI.
"""
import time
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import DefaultDict, Dict

from redis import Redis


@dataclass
class RateLimit:
    """Rate limit configuration."""
    max_requests: int
    window_seconds: int


class InMemoryRateLimiter:
    """Simple in-memory rate limiter using token bucket algorithm."""

    def __init__(self):
        """Initialize rate limiter."""
        self.requests: DefaultDict[str, Dict[datetime, int]] = defaultdict(dict)

    def is_allowed(self, key: str, limit: RateLimit) -> bool:
        """Check if request is allowed under rate limit.

        Args:
            key: Identifier for the rate limit bucket.
            limit: Rate limit configuration.

        Returns:
            Whether request is allowed.
        """
        now = datetime.now()
        window_start = now - timedelta(seconds=limit.window_seconds)
        
        # Clean up old requests
        self.requests[key] = {
            ts: count
            for ts, count in self.requests[key].items()
            if ts > window_start
        }
        
        # Count recent requests
        total_requests = sum(self.requests[key].values())
        
        # Check if under limit
        if total_requests < limit.max_requests:
            self.requests[key][now] = self.requests[key].get(now, 0) + 1
            return True
        
        return False


class RedisRateLimiter:
    """Distributed rate limiter using Redis."""

    def __init__(self, redis_url: str = "redis://localhost:6379/0"):
        """Initialize rate limiter.

        Args:
            redis_url: Redis connection URL.
        """
        self.redis = Redis.from_url(redis_url)

    def is_allowed(self, key: str, limit: RateLimit) -> bool:
        """Check if request is allowed under rate limit.

        Args:
            key: Identifier for the rate limit bucket.
            limit: Rate limit configuration.

        Returns:
            Whether request is allowed.
        """
        pipe = self.redis.pipeline()
        now = int(time.time())
        window_start = now - limit.window_seconds
        
        # Remove old requests
        pipe.zremrangebyscore(key, 0, window_start)
        
        # Count recent requests
        pipe.zcard(key)
        
        # Add current request
        pipe.zadd(key, {str(now): now})
        
        # Set expiry on the key
        pipe.expire(key, limit.window_seconds)
        
        # Execute pipeline
        _, current_requests, *_ = pipe.execute()
        
        return current_requests < limit.max_requests


class RateLimitDecorator:
    """Decorator for rate limiting functions."""

    def __init__(
        self,
        max_requests: int,
        window_seconds: int,
        key_func=None,
        redis_url: str | None = None,
    ):
        """Initialize rate limit decorator.

        Args:
            max_requests: Maximum number of requests allowed.
            window_seconds: Time window in seconds.
            key_func: Function to generate rate limit key.
            redis_url: Redis URL for distributed rate limiting.
        """
        self.limit = RateLimit(max_requests, window_seconds)
        self.key_func = key_func or (lambda *args, **kwargs: "default")
        self.limiter = (
            RedisRateLimiter(redis_url)
            if redis_url
            else InMemoryRateLimiter()
        )

    def __call__(self, func):
        """Apply rate limiting to function.

        Args:
            func: Function to rate limit.

        Returns:
            Rate limited function.
        """
        def wrapper(*args, **kwargs):
            key = self.key_func(*args, **kwargs)
            if not self.limiter.is_allowed(key, self.limit):
                raise Exception(
                    f"Rate limit exceeded: {self.limit.max_requests} "
                    f"requests per {self.limit.window_seconds} seconds"
                )
            return func(*args, **kwargs)
        return wrapper