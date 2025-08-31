"""
Google Trends API Module
Core API wrapper for Google Trends data access
"""

from .trends_api import GoogleTrendsAPI
from .trends_client import TrendsClient
from .data_analyzer import DataAnalyzer
from .rate_limiter import RateLimiter

__all__ = [
    "GoogleTrendsAPI",
    "TrendsClient", 
    "DataAnalyzer",
    "RateLimiter"
]
