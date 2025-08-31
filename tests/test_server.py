"""
Tests for Google Trends MCP Server
"""

import pytest
import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from google_trends_mcp.server import GoogleTrendsMCPServer
from google_trends_mcp.models import TrendData, RelatedQuery, RegionInterest
from google_trends_mcp.utils import AVAILABLE_TIMEFRAMES, AVAILABLE_REGIONS


class TestGoogleTrendsMCPServer:
    """Test cases for Google Trends MCP Server."""
    
    def test_server_initialization(self):
        """Test server initialization."""
        server = GoogleTrendsMCPServer()
        assert server is not None
        assert server.trends_api is None
    
    def test_available_timeframes(self):
        """Test available timeframes."""
        assert len(AVAILABLE_TIMEFRAMES) == 9
        assert 'today 12-m' in AVAILABLE_TIMEFRAMES
        assert '2004-present' in AVAILABLE_TIMEFRAMES
    
    def test_available_regions(self):
        """Test available regions."""
        assert len(AVAILABLE_REGIONS) == 30
        assert 'US' in AVAILABLE_REGIONS
        assert 'GB' in AVAILABLE_REGIONS
        assert 'CA' in AVAILABLE_REGIONS


class TestDataModels:
    """Test cases for data models."""
    
    def test_trend_data_model(self):
        """Test TrendData model."""
        trend_data = TrendData(
            keyword="python",
            mean_interest=61.47,
            peak_interest=100,
            peak_date="2025-07-31",
            data_points=93,
            date_range="2025-05-31 to 2025-08-31"
        )
        assert trend_data.keyword == "python"
        assert trend_data.mean_interest == 61.47
    
    def test_related_query_model(self):
        """Test RelatedQuery model."""
        related_query = RelatedQuery(
            query="python list",
            value=100,
            type="top"
        )
        assert related_query.query == "python list"
        assert related_query.value == 100
        assert related_query.type == "top"
    
    def test_region_interest_model(self):
        """Test RegionInterest model."""
        region_interest = RegionInterest(
            region="Washington",
            interest=100,
            keyword="python"
        )
        assert region_interest.region == "Washington"
        assert region_interest.interest == 100
        assert region_interest.keyword == "python"


if __name__ == "__main__":
    pytest.main([__file__])
