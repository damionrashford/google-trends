"""
Tool Factory Component
Creates and configures MCP tools with proper dependencies
"""

from typing import List, Optional, Dict, Any
from mcp.server.session import ServerSession
from mcp.server.fastmcp import Context

from ..api import GoogleTrendsAPI
from ..models import (
    TrendData, RelatedQuery, RegionInterest, 
    ExportResult, SQLTableResult, ComparisonResult
)
from ..utils import (
    AVAILABLE_TIMEFRAMES, AVAILABLE_REGIONS,
    generate_filename, create_export_directory, sanitize_table_name
)


class ToolFactory:
    """Creates and configures MCP tools with proper dependencies."""
    
    def __init__(self, trends_api: GoogleTrendsAPI):
        """
        Initialize the tool factory.
        
        Args:
            trends_api: Google Trends API instance
        """
        self.trends_api = trends_api
    
    def create_search_trends_tool(self):
        """Create the search_trends tool."""
        async def search_trends(
            keywords: List[str],
            timeframe: str = "today 12-m",
            geo: str = "US",
            ctx: Context[ServerSession, None] = None,
        ) -> List[TrendData]:
            """
            Search for Google Trends data for given keywords.
            
            Args:
                keywords: List of search terms to analyze
                timeframe: Time range (e.g., 'today 12-m', 'today 5-y', 'now 1-d')
                geo: Geographic location (e.g., 'US', 'GB', 'CA')
            
            Returns:
                List of trend data for each keyword
            """
            if ctx:
                await ctx.info(f"Searching trends for keywords: {keywords}")
            
            try:
                data = self.trends_api.search_trends(keywords, timeframe, geo)
                
                if data.empty:
                    return []
                
                results = []
                for keyword in keywords:
                    if keyword in data.columns:
                        stats = self.trends_api.get_statistics(data[[keyword]])
                        if keyword in stats:
                            stat = stats[keyword]
                            results.append(TrendData(
                                keyword=keyword,
                                mean_interest=stat['mean'],
                                peak_interest=stat['peak_value'],
                                peak_date=stat['peak_date'],
                                data_points=stat['total_points'],
                                date_range=f"{data.index[0].strftime('%Y-%m-%d')} to {data.index[-1].strftime('%Y-%m-%d')}"
                            ))
                
                if ctx:
                    await ctx.info(f"Retrieved trend data for {len(results)} keywords")
                
                return results
                
            except Exception as e:
                if ctx:
                    await ctx.error(f"Error searching trends: {str(e)}")
                raise
        
        return search_trends
    
    def create_related_queries_tool(self):
        """Create the get_related_queries tool."""
        async def get_related_queries(
            keyword: str,
            timeframe: str = "today 12-m",
            geo: str = "US",
            ctx: Context[ServerSession, None] = None,
        ) -> List[RelatedQuery]:
            """
            Get related queries for a keyword.
            
            Args:
                keyword: Search term to find related queries for
                timeframe: Time range for analysis
                geo: Geographic location
            
            Returns:
                List of related queries with interest values
            """
            if ctx:
                await ctx.info(f"Getting related queries for: {keyword}")
            
            try:
                related = self.trends_api.get_related_queries([keyword], timeframe, geo)
                
                results = []
                if keyword in related:
                    data = related[keyword]
                    
                    # Add top queries
                    if 'top' in data and not data['top'].empty:
                        for _, row in data['top'].head(10).iterrows():
                            results.append(RelatedQuery(
                                query=row['query'],
                                value=row['value'],
                                type='top'
                            ))
                    
                    # Add rising queries
                    if 'rising' in data and not data['rising'].empty:
                        for _, row in data['rising'].head(10).iterrows():
                            results.append(RelatedQuery(
                                query=row['query'],
                                value=row['value'],
                                type='rising'
                            ))
                
                if ctx:
                    await ctx.info(f"Found {len(results)} related queries")
                
                return results
                
            except Exception as e:
                if ctx:
                    await ctx.error(f"Error getting related queries: {str(e)}")
                raise
        
        return get_related_queries
    
    def create_export_tools(self):
        """Create export-related tools."""
        
        async def export_trends_to_csv(
            keywords: List[str],
            timeframe: str = "today 12-m",
            geo: str = "US",
            filename: Optional[str] = None,
            ctx: Context[ServerSession, None] = None,
        ) -> ExportResult:
            """Export Google Trends data to CSV file."""
            if ctx:
                await ctx.info(f"Exporting trends data for: {keywords}")
            
            try:
                data = self.trends_api.search_trends(keywords, timeframe, geo)
                
                if data.empty:
                    raise ValueError("No data to export")
                
                # Generate filename
                filename = generate_filename("trends", keywords, "csv", filename)
                
                # Create export directory
                export_dir = create_export_directory("google_trends_exports")
                file_path = export_dir / filename
                
                # Export data
                data.to_csv(file_path, index=True)
                
                # Get file size
                size_bytes = file_path.stat().st_size
                
                if ctx:
                    await ctx.info(f"Exported {len(data)} data points to {filename}")
                
                return ExportResult(
                    filename=filename,
                    format="csv",
                    size_bytes=size_bytes,
                    path=str(file_path)
                )
                
            except Exception as e:
                if ctx:
                    await ctx.error(f"Error exporting to CSV: {str(e)}")
                raise
        
        return export_trends_to_csv
    
    def create_utility_tools(self):
        """Create utility tools."""
        
        async def get_available_timeframes(ctx: Context[ServerSession, None] = None) -> List[str]:
            """Get list of available timeframes for Google Trends queries."""
            if ctx:
                await ctx.info(f"Available timeframes: {len(AVAILABLE_TIMEFRAMES)} options")
            return AVAILABLE_TIMEFRAMES
        
        async def get_available_regions(ctx: Context[ServerSession, None] = None) -> List[str]:
            """Get list of available geographic regions."""
            if ctx:
                await ctx.info(f"Available regions: {len(AVAILABLE_REGIONS)} countries")
            return AVAILABLE_REGIONS
        
        return get_available_timeframes, get_available_regions
