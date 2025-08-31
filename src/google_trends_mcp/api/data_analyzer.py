"""
Data Analyzer Component
Handles data analysis and statistics calculations
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List
from datetime import datetime


class DataAnalyzer:
    """Handles data analysis and statistics calculations."""
    
    @staticmethod
    def get_statistics(data: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
        """
        Calculate comprehensive statistics for trend data.
        
        Args:
            data: DataFrame with trend data
            
        Returns:
            Dict containing statistics for each column
        """
        stats = {}
        
        for column in data.columns:
            if column == 'isPartial':
                continue
                
            series = data[column].dropna()
            
            if series.empty:
                stats[column] = {
                    'mean': 0.0,
                    'median': 0.0,
                    'std': 0.0,
                    'min': 0,
                    'max': 0,
                    'peak_value': 0,
                    'peak_date': None,
                    'total_points': 0,
                    'trend_direction': 'stable',
                    'volatility': 0.0
                }
                continue
            
            # Basic statistics
            mean_val = series.mean()
            median_val = series.median()
            std_val = series.std()
            min_val = series.min()
            max_val = series.max()
            
            # Peak analysis
            peak_idx = series.idxmax()
            peak_value = series.max()
            peak_date = peak_idx.strftime('%Y-%m-%d') if hasattr(peak_idx, 'strftime') else str(peak_idx)
            
            # Trend analysis
            trend_direction = DataAnalyzer._calculate_trend_direction(series)
            
            # Volatility (coefficient of variation)
            volatility = (std_val / mean_val) * 100 if mean_val > 0 else 0
            
            stats[column] = {
                'mean': round(mean_val, 2),
                'median': round(median_val, 2),
                'std': round(std_val, 2),
                'min': int(min_val),
                'max': int(max_val),
                'peak_value': int(peak_value),
                'peak_date': peak_date,
                'total_points': len(series),
                'trend_direction': trend_direction,
                'volatility': round(volatility, 2)
            }
        
        return stats
    
    @staticmethod
    def _calculate_trend_direction(series: pd.Series) -> str:
        """
        Calculate trend direction based on linear regression.
        
        Args:
            series: Time series data
            
        Returns:
            Trend direction: 'increasing', 'decreasing', or 'stable'
        """
        if len(series) < 2:
            return 'stable'
        
        # Simple linear trend calculation
        x = np.arange(len(series))
        y = series.values
        
        # Calculate slope
        slope = np.polyfit(x, y, 1)[0]
        
        # Determine trend direction
        if slope > 0.5:
            return 'increasing'
        elif slope < -0.5:
            return 'decreasing'
        else:
            return 'stable'
    
    @staticmethod
    def compare_keywords(data: pd.DataFrame, keywords: List[str]) -> Dict[str, Any]:
        """
        Compare multiple keywords and provide insights.
        
        Args:
            data: DataFrame with trend data
            keywords: List of keywords to compare
            
        Returns:
            Comparison analysis
        """
        if data.empty or not keywords:
            return {}
        
        comparison = {
            'keywords': keywords,
            'comparison_date': datetime.now().isoformat(),
            'total_data_points': len(data),
            'date_range': f"{data.index[0].strftime('%Y-%m-%d')} to {data.index[-1].strftime('%Y-%m-%d')}",
            'keyword_stats': {},
            'rankings': {}
        }
        
        # Calculate statistics for each keyword
        stats = DataAnalyzer.get_statistics(data)
        
        for keyword in keywords:
            if keyword in stats:
                comparison['keyword_stats'][keyword] = stats[keyword]
        
        # Create rankings
        if comparison['keyword_stats']:
            # Average interest ranking
            avg_interest = {k: v['mean'] for k, v in comparison['keyword_stats'].items()}
            comparison['rankings']['by_average_interest'] = sorted(
                avg_interest.items(), key=lambda x: x[1], reverse=True
            )
            
            # Peak interest ranking
            peak_interest = {k: v['peak_value'] for k, v in comparison['keyword_stats'].items()}
            comparison['rankings']['by_peak_interest'] = sorted(
                peak_interest.items(), key=lambda x: x[1], reverse=True
            )
            
            # Volatility ranking
            volatility = {k: v['volatility'] for k, v in comparison['keyword_stats'].items()}
            comparison['rankings']['by_volatility'] = sorted(
                volatility.items(), key=lambda x: x[1], reverse=True
            )
        
        return comparison
    
    @staticmethod
    def get_seasonal_patterns(data: pd.DataFrame, keyword: str) -> Dict[str, Any]:
        """
        Analyze seasonal patterns in trend data.
        
        Args:
            data: DataFrame with trend data
            keyword: Keyword to analyze
            
        Returns:
            Seasonal pattern analysis
        """
        if data.empty or keyword not in data.columns:
            return {}
        
        series = data[keyword].dropna()
        
        if len(series) < 30:  # Need sufficient data for seasonal analysis
            return {}
        
        # Monthly patterns
        monthly_avg = series.groupby(series.index.month).mean()
        
        # Weekly patterns (if we have daily data)
        weekly_avg = None
        if len(series) > 7:
            weekly_avg = series.groupby(series.index.dayofweek).mean()
        
        return {
            'keyword': keyword,
            'monthly_patterns': monthly_avg.to_dict(),
            'weekly_patterns': weekly_avg.to_dict() if weekly_avg is not None else None,
            'seasonal_peaks': monthly_avg.nlargest(3).index.tolist(),
            'seasonal_lows': monthly_avg.nsmallest(3).index.tolist()
        }
