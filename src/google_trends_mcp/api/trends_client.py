"""
Trends Client Component
Handles core Google Trends API interactions
"""

from typing import List, Dict, Optional
import pandas as pd
from pytrends.request import TrendReq
import requests

from .rate_limiter import RateLimiter


class TrendsClient:
    """Handles core Google Trends API interactions."""
    
    def __init__(self, hl: str = 'en-US', tz: int = 360, timeout: tuple = (10, 25), 
                 retries: int = 3, backoff_factor: float = 0.3):
        """
        Initialize the trends client.
        
        Args:
            hl: Language (default: 'en-US')
            tz: Timezone offset in minutes (default: 360 for EST)
            timeout: Request timeout (connect, read)
            retries: Number of retries for failed requests
            backoff_factor: Backoff factor for retries
        """
        self.pytrends = TrendReq(hl=hl, tz=tz, timeout=timeout, retries=retries, backoff_factor=backoff_factor)
        self.hl = hl
        self.tz = tz
        self.session = requests.Session()
        self.rate_limiter = RateLimiter()
    
    def search_trends(self, keywords: List[str], timeframe: str = 'today 12-m', 
                     geo: str = '', cat: int = 0) -> pd.DataFrame:
        """
        Search for trends data for given keywords.
        
        Args:
            keywords: List of search terms
            timeframe: Time range for data (e.g., 'today 12-m', 'today 5-y')
            geo: Geographic location (e.g., 'US', 'GB')
            cat: Category ID (0 for all categories)
            
        Returns:
            pd.DataFrame: Trends data
        """
        def _fetch_trends():
            self.pytrends.build_payload(keywords, cat=cat, timeframe=timeframe, geo=geo)
            return self.pytrends.interest_over_time()
        
        self.rate_limiter.wait_for_rate_limit()
        result = self.rate_limiter.retry_with_backoff(_fetch_trends)
        
        if result.empty:
            print(f"No data found for keywords: {keywords}")
            
        return result
    
    def get_related_queries(self, keywords: List[str], timeframe: str = 'today 12-m', 
                           geo: str = '', cat: int = 0) -> Dict:
        """
        Get related queries for given keywords.
        
        Args:
            keywords: List of search terms
            timeframe: Time range for data
            geo: Geographic location
            cat: Category ID
            
        Returns:
            Dict: Related queries data
        """
        def _fetch_related_queries():
            self.pytrends.build_payload(keywords, cat=cat, timeframe=timeframe, geo=geo)
            return self.pytrends.related_queries()
        
        self.rate_limiter.wait_for_rate_limit()
        return self.rate_limiter.retry_with_backoff(_fetch_related_queries)
    
    def get_interest_by_region(self, keywords: List[str], resolution: str = 'COUNTRY',
                              timeframe: str = 'today 12-m', geo: str = '', cat: int = 0) -> pd.DataFrame:
        """
        Get interest by region for given keywords.
        
        Args:
            keywords: List of search terms
            resolution: Geographic resolution ('COUNTRY', 'REGION', 'CITY', 'DMA')
            timeframe: Time range for data
            geo: Geographic location
            cat: Category ID
            
        Returns:
            pd.DataFrame: Interest by region data
        """
        def _fetch_interest_by_region():
            self.pytrends.build_payload(keywords, cat=cat, timeframe=timeframe, geo=geo)
            return self.pytrends.interest_by_region(resolution=resolution)
        
        self.rate_limiter.wait_for_rate_limit()
        return self.rate_limiter.retry_with_backoff(_fetch_interest_by_region)
    
    def get_trending_searches(self, geo: str = 'US') -> List[str]:
        """
        Get trending searches for a specific location.
        
        Args:
            geo: Geographic location (default: 'US')
            
        Returns:
            List[str]: List of trending search terms
        """
        try:
            trending_searches = self.pytrends.trending_searches(pn=geo)
            return trending_searches[0].tolist()
        except Exception as e:
            print(f"Error fetching trending searches: {e}")
            return []
