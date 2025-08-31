"""
Rate Limiter Component
Handles rate limiting and retry logic for Google Trends API
"""

import time
from typing import Any, Callable
import pandas as pd


class RateLimiter:
    """Handles rate limiting and retry logic for API requests."""
    
    def __init__(self, request_delay: float = 5.0, max_retries: int = 5, base_delay: float = 10.0):
        """
        Initialize the rate limiter.
        
        Args:
            request_delay: Delay between requests in seconds
            max_retries: Maximum number of retry attempts
            base_delay: Base delay for exponential backoff
        """
        self.request_delay = request_delay
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.last_request_time = 0
    
    def wait_for_rate_limit(self):
        """Wait appropriate time between requests to avoid rate limiting."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.request_delay:
            sleep_time = self.request_delay - time_since_last
            print(f"Waiting {sleep_time:.1f} seconds to avoid rate limiting...")
            time.sleep(sleep_time)
        self.last_request_time = time.time()
    
    def retry_with_backoff(self, func: Callable, *args, **kwargs) -> Any:
        """
        Retry function with exponential backoff for rate limiting.
        
        Args:
            func: Function to retry
            *args: Function arguments
            **kwargs: Function keyword arguments
            
        Returns:
            Function result or empty DataFrame/Dict on failure
        """
        for attempt in range(self.max_retries):
            try:
                # Add delay between requests
                if attempt > 0:
                    delay = self.base_delay * (2 ** attempt)
                    print(f"Rate limited, retrying in {delay} seconds... (attempt {attempt + 1}/{self.max_retries})")
                    time.sleep(delay)
                
                result = func(*args, **kwargs)
                
                # Check if result is empty but no exception was raised
                if hasattr(result, 'empty') and result.empty:
                    print(f"Empty result received, retrying... (attempt {attempt + 1}/{self.max_retries})")
                    continue
                    
                return result
                
            except Exception as e:
                error_msg = str(e).lower()
                if '429' in error_msg or 'too many requests' in error_msg:
                    print(f"Rate limited, retrying... (attempt {attempt + 1}/{self.max_retries})")
                    if attempt == self.max_retries - 1:
                        print(f"Max retries exceeded for rate limiting: {e}")
                        return self._get_empty_result(func)
                else:
                    print(f"Error on attempt {attempt + 1}: {e}")
                    if attempt == self.max_retries - 1:
                        return self._get_empty_result(func)
        
        return self._get_empty_result(func)
    
    def _get_empty_result(self, func: Callable) -> Any:
        """Get appropriate empty result based on function type."""
        if 'trends' in func.__name__ or 'interest' in func.__name__:
            return pd.DataFrame()
        else:
            return {}
