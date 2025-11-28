import time
from functools import wraps

class RateLimiter:
    """
    Enforces a strict rate limit.
    """
    def __init__(self, requests_per_minute, buffer_seconds=0.5):
        self.delay = (60.0 / requests_per_minute) + buffer_seconds
        self.last_call_timestamp = 0

    def wait(self):
        """Blocks execution until safe to proceed."""
        current_time = time.time()
        time_passed = current_time - self.last_call_timestamp
        
        if time_passed < self.delay:
            sleep_time = self.delay - time_passed
            # Only print if sleep is significant (>1s) to reduce noise
            if sleep_time > 1:
                print(f"🚦 Rate Limit: Sleeping for {sleep_time:.2f}s...")
            time.sleep(sleep_time)
        
        self.last_call_timestamp = time.time()

# Gemini 2.5 Flash Free Tier is often stricter (approx 10-15 RPM)
chat_limiter = RateLimiter(requests_per_minute=10, buffer_seconds=1.0)

# Embedding models usually allow higher throughput (e.g., 60-100 RPM)
embed_limiter = RateLimiter(requests_per_minute=100, buffer_seconds=0.1)

def rate_limited(limiter):
    """Decorator factory that accepts a specific limiter."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            limiter.wait()
            return func(*args, **kwargs)
        return wrapper
    return decorator