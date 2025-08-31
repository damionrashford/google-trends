"""
Google Trends API Wrapper using pytrends
Provides complete access to Google Trends data for various use cases
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Optional, Tuple, Union, Any
import time
import json
from datetime import datetime, timedelta
import requests
import warnings
warnings.filterwarnings('ignore')
import numpy as np

from .trends_client import TrendsClient
from .data_analyzer import DataAnalyzer

# Set matplotlib style
try:
    plt.style.use('seaborn-v0_8')
except:
    plt.style.use('seaborn')


class GoogleTrendsAPI:
    """
    A comprehensive wrapper for Google Trends data using pytrends
    Provides access to all Google Trends functionality
    """
    
    def __init__(self, hl='en-US', tz=360, timeout=(10, 25), retries=3, backoff_factor=0.3):
        """
        Initialize the Google Trends API wrapper
        
        Args:
            hl (str): Language (default: 'en-US')
            tz (int): Timezone offset in minutes (default: 360 for EST)
            timeout (tuple): Request timeout (connect, read)
            retries (int): Number of retries for failed requests
            backoff_factor (float): Backoff factor for retries
        """
        self.client = TrendsClient(hl=hl, tz=tz, timeout=timeout, retries=retries, backoff_factor=backoff_factor)
        self.analyzer = DataAnalyzer()
        
        self.hl = hl
        self.tz = tz
        
    def search_trends(self, keywords: List[str], timeframe: str = 'today 12-m', 
                     geo: str = '', cat: int = 0) -> pd.DataFrame:
        """
        Search for trends data for given keywords
        
        Args:
            keywords (List[str]): List of search terms
            timeframe (str): Time range for data (e.g., 'today 12-m', 'today 5-y')
            geo (str): Geographic location (e.g., 'US', 'GB')
            cat (int): Category ID (0 for all categories)
            
        Returns:
            pd.DataFrame: Trends data
        """
        return self.client.search_trends(keywords, timeframe, geo, cat)
    
    def get_interest_over_time(self, keywords: List[str], timeframe: str = 'today 12-m', 
                              geo: str = '', cat: int = 0) -> pd.DataFrame:
        """
        Get interest over time data (alias for search_trends)
        
        Args:
            keywords (List[str]): List of search terms
            timeframe (str): Time range for data
            geo (str): Geographic location
            cat (int): Category ID
            
        Returns:
            pd.DataFrame: Interest over time data
        """
        return self.search_trends(keywords, timeframe, geo, cat)
    
    def get_related_queries(self, keywords: List[str], timeframe: str = 'today 12-m', 
                           geo: str = '', cat: int = 0) -> Dict:
        """
        Get related queries for given keywords
        
        Args:
            keywords (List[str]): List of search terms
            timeframe (str): Time range for data
            geo (str): Geographic location
            cat (int): Category ID
            
        Returns:
            Dict: Related queries data
        """
        return self.client.get_related_queries(keywords, timeframe, geo, cat)
    
    def get_related_topics(self, keywords: List[str], timeframe: str = 'today 12-m', 
                          geo: str = '', cat: int = 0) -> Dict:
        """
        Get related topics for given keywords
        
        Args:
            keywords (List[str]): List of search terms
            timeframe (str): Time range for data
            geo (str): Geographic location
            cat (int): Category ID
            
        Returns:
            Dict: Related topics data
        """
        try:
            self.client.pytrends.build_payload(keywords, cat=cat, timeframe=timeframe, geo=geo)
            related_topics = self.client.pytrends.related_topics()
            return related_topics
            
        except Exception as e:
            print(f"Error fetching related topics: {e}")
            return {}
    
    def get_trending_searches(self, geo: str = 'US') -> List[str]:
        """
        Get trending searches for a specific location
        
        Args:
            geo (str): Geographic location (default: 'US')
            
        Returns:
            List[str]: List of trending search terms
        """
        return self.client.get_trending_searches(geo)
    
    def get_realtime_trending_searches(self, geo: str = 'US', cat: str = 'all') -> pd.DataFrame:
        """
        Get real-time trending searches
        
        Args:
            geo (str): Geographic location (default: 'US')
            cat (str): Category (default: 'all')
            
        Returns:
            pd.DataFrame: Real-time trends data
        """
        try:
            realtime_trends = self.client.pytrends.realtime_trending_searches(pn=geo, cat=cat)
            return realtime_trends
            
        except Exception as e:
            print(f"Error fetching real-time trends: {e}")
            return pd.DataFrame()
    
    def get_interest_by_region(self, keywords: List[str], resolution: str = 'COUNTRY',
                              timeframe: str = 'today 12-m', geo: str = '', cat: int = 0) -> pd.DataFrame:
        """
        Get interest by region for given keywords
        
        Args:
            keywords (List[str]): List of search terms
            resolution (str): Geographic resolution ('COUNTRY', 'REGION', 'CITY', 'DMA')
            timeframe (str): Time range for data
            geo (str): Geographic location
            cat (int): Category ID
            
        Returns:
            pd.DataFrame: Interest by region data
        """
        return self.client.get_interest_by_region(keywords, resolution, timeframe, geo, cat)
    
    def get_statistics(self, data: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """
        Get comprehensive statistics for trend data
        
        Args:
            data (pd.DataFrame): Trends data
            
        Returns:
            Dict: Statistics for each keyword
        """
        return self.analyzer.get_statistics(data)
    
    def compare_keywords(self, keywords: List[str], timeframe: str = 'today 12-m', 
                        geo: str = 'US') -> Dict[str, Any]:
        """
        Compare multiple keywords with comprehensive analysis
        
        Args:
            keywords (List[str]): List of keywords to compare
            timeframe (str): Time range for analysis
            geo (str): Geographic location
            
        Returns:
            Dict: Comprehensive comparison analysis
        """
        data = self.search_trends(keywords, timeframe, geo)
        return self.analyzer.compare_keywords(data, keywords)
    
    def get_seasonal_patterns(self, data: pd.DataFrame, keyword: str) -> Dict[str, Any]:
        """
        Analyze seasonal patterns in trend data
        
        Args:
            data (pd.DataFrame): Trends data
            keyword (str): Keyword to analyze
            
        Returns:
            Dict: Seasonal pattern analysis
        """
        return self.analyzer.get_seasonal_patterns(data, keyword)
    
    # Additional methods for backward compatibility
    def get_top_charts(self, date: str = '202401', hl: str = 'en-US', tz: int = 300, geo: str = 'US') -> pd.DataFrame:
        """Get top charts data"""
        try:
            top_charts = self.client.pytrends.top_charts(date=date, hl=hl, tz=tz, geo=geo)
            return top_charts
        except Exception as e:
            print(f"Error fetching top charts: {e}")
            return pd.DataFrame()
    
    def get_suggestions(self, keyword: str) -> List[str]:
        """Get search suggestions for a keyword"""
        try:
            suggestions = self.client.pytrends.suggestions(keyword)
            return [suggestion['title'] for suggestion in suggestions]
        except Exception as e:
            print(f"Error fetching suggestions: {e}")
            return []
    
    def get_categories(self) -> Dict:
        """Get available categories"""
        try:
            categories = self.client.pytrends.categories()
            return categories
        except Exception as e:
            print(f"Error fetching categories: {e}")
            return {}
    
    def get_today_searches(self, geo: str = 'US') -> List[str]:
        """Get today's searches for a location"""
        try:
            today_searches = self.client.pytrends.today_searches(pn=geo)
            return today_searches[0].tolist()
        except Exception as e:
            print(f"Error fetching today's searches: {e}")
            return []
    
    def plot_trends(self, data: pd.DataFrame, title: str = "Google Trends Data", 
                   figsize: Tuple[int, int] = (12, 6), save_path: Optional[str] = None,
                   style: str = 'default'):
        """
        Plot trends data
        
        Args:
            data (pd.DataFrame): Trends data to plot
            title (str): Plot title
            figsize (Tuple[int, int]): Figure size
            save_path (Optional[str]): Path to save the plot
            style (str): Plot style
        """
        if data.empty:
            print("No data to plot")
            return
            
        plt.figure(figsize=figsize)
        
        # Remove 'isPartial' column if it exists
        plot_data = data.drop('isPartial', axis=1, errors='ignore')
        
        colors = plt.cm.Set3(np.linspace(0, 1, len(plot_data.columns)))
        
        for i, column in enumerate(plot_data.columns):
            plt.plot(plot_data.index, plot_data[column], label=column, 
                    linewidth=2, color=colors[i])
        
        plt.title(title, fontsize=16, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Interest Over Time', fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {save_path}")
        
        plt.show()
    
    def plot_interest_by_region(self, data: pd.DataFrame, title: str = "Interest by Region", 
                               top_n: int = 10, figsize: Tuple[int, int] = (12, 8),
                               save_path: Optional[str] = None):
        """
        Plot interest by region data
        
        Args:
            data (pd.DataFrame): Interest by region data
            title (str): Plot title
            top_n (int): Number of top regions to show
            figsize (Tuple[int, int]): Figure size
            save_path (Optional[str]): Path to save the plot
        """
        if data.empty:
            print("No data to plot")
            return
            
        # Get the first keyword's data
        keyword = data.columns[0]
        top_regions = data.nlargest(top_n, keyword)
        
        plt.figure(figsize=figsize)
        bars = plt.barh(range(len(top_regions)), top_regions[keyword])
        plt.yticks(range(len(top_regions)), top_regions.index)
        plt.xlabel('Interest', fontsize=12)
        plt.title(f"{title} - {keyword}", fontsize=16, fontweight='bold')
        plt.gca().invert_yaxis()
        
        # Add value labels on bars
        for i, bar in enumerate(bars):
            width = bar.get_width()
            plt.text(width + 0.5, bar.get_y() + bar.get_height()/2, 
                    f'{int(width)}', ha='left', va='center')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {save_path}")
        
        plt.show()
    
    def plot_heatmap(self, data: pd.DataFrame, title: str = "Trends Heatmap",
                    figsize: Tuple[int, int] = (14, 8), save_path: Optional[str] = None):
        """
        Create a heatmap of trends data
        
        Args:
            data (pd.DataFrame): Trends data
            title (str): Plot title
            figsize (Tuple[int, int]): Figure size
            save_path (Optional[str]): Path to save the plot
        """
        if data.empty:
            print("No data to plot")
            return
            
        # Remove 'isPartial' column if it exists
        plot_data = data.drop('isPartial', axis=1, errors='ignore')
        
        # Resample to monthly data for better heatmap visualization
        monthly_data = plot_data.resample('M').mean()
        
        plt.figure(figsize=figsize)
        sns.heatmap(monthly_data.T, cmap='YlOrRd', annot=False, cbar_kws={'label': 'Interest'})
        plt.title(title, fontsize=16, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Keywords', fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Plot saved to {save_path}")
        
        plt.show()
    
    def export_data(self, data: pd.DataFrame, filename: str, format: str = 'csv'):
        """
        Export data to file
        
        Args:
            data (pd.DataFrame): Data to export
            filename (str): Output filename
            format (str): Export format ('csv', 'json', 'excel')
        """
        try:
            if format.lower() == 'csv':
                data.to_csv(filename)
            elif format.lower() == 'json':
                data.to_json(filename)
            elif format.lower() == 'excel':
                data.to_excel(filename)
            else:
                print(f"Unsupported format: {format}")
                return
                
            print(f"Data exported to {filename}")
            
        except Exception as e:
            print(f"Error exporting data: {e}")


# Utility functions
def create_trends_api() -> GoogleTrendsAPI:
    """Create and return a Google Trends API instance"""
    return GoogleTrendsAPI()


def quick_trend_search(keyword: str, timeframe: str = 'today 12-m', geo: str = '') -> pd.DataFrame:
    """
    Quick function to search for a single keyword
    
    Args:
        keyword (str): Search term
        timeframe (str): Time range
        geo (str): Geographic location
        
    Returns:
        pd.DataFrame: Trends data
    """
    api = GoogleTrendsAPI()
    return api.search_trends([keyword], timeframe, geo)


def get_available_timeframes() -> List[str]:
    """
    Get list of available timeframes
    
    Returns:
        List[str]: Available timeframes
    """
    return [
        'now 1-H',    # Past hour
        'now 4-H',    # Past 4 hours
        'now 1-d',    # Past day
        'now 7-d',    # Past 7 days
        'today 1-m',  # Past month
        'today 3-m',  # Past 3 months
        'today 12-m', # Past 12 months
        'today 5-y',  # Past 5 years
        '2004-present' # All time
    ]


def get_available_regions() -> List[str]:
    """
    Get list of available regions
    
    Returns:
        List[str]: Available regions
    """
    return [
        'US', 'GB', 'CA', 'AU', 'DE', 'FR', 'IT', 'ES', 'NL', 'BR',
        'MX', 'AR', 'CL', 'CO', 'PE', 'VE', 'JP', 'KR', 'IN', 'SG',
        'MY', 'TH', 'VN', 'PH', 'ID', 'NZ', 'ZA', 'EG', 'NG', 'KE'
    ]


if __name__ == "__main__":
    # Example usage
    api = GoogleTrendsAPI()
    
    # Search for trends
    data = api.search_trends(['python', 'javascript'], 'today 12-m', 'US')
    print("Trends data:")
    print(data.head())
    
    # Plot the data
    api.plot_trends(data, "Python vs JavaScript Trends")
    
    # Get trending searches
    trending = api.get_trending_searches('US')
    print(f"\nTrending searches in US: {trending[:5]}")
    
    # Get comprehensive comparison
    comparison = api.compare_keywords(['bitcoin', 'ethereum'], 'today 12-m', 'US')
    print(f"\nComparison statistics: {comparison['statistics']}")
