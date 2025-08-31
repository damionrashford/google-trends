"""
Google Trends MCP Server
Model Context Protocol server implementation
"""

import asyncio
import json
import sqlite3
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
from mcp.server.fastmcp import Context, FastMCP
from mcp.server.session import ServerSession

from ..api import GoogleTrendsAPI
from ..models import (
    TrendData, RelatedQuery, RegionInterest, 
    ExportResult, SQLTableResult, ComparisonResult
)
from ..utils import (
    AVAILABLE_TIMEFRAMES, AVAILABLE_REGIONS,
    generate_filename, create_export_directory, sanitize_table_name
)

from .tool_registry import ToolRegistry
from .tool_factory import ToolFactory


class GoogleTrendsMCPServer:
    """Google Trends MCP Server implementation."""
    
    def __init__(self):
        """Initialize the MCP server."""
        self.mcp = FastMCP(
            name="Google Trends API",
            instructions="""A comprehensive Google Trends API server that provides access to search trend data, 
            related queries, geographic interest, and data export capabilities. Use this server to analyze 
            search trends, compare keywords, and export data for further analysis.""",
        )
        
        self.trends_api: Optional[GoogleTrendsAPI] = None
        self.tool_registry: Optional[ToolRegistry] = None
        self.tool_factory: Optional[ToolFactory] = None
        self._initialize_components()
        self._register_tools()
    
    def _initialize_components(self):
        """Initialize server components."""
        if self.trends_api is None:
            self.trends_api = GoogleTrendsAPI()
        
        self.tool_registry = ToolRegistry(self.mcp)
        self.tool_factory = ToolFactory(self.trends_api)
    
    def _register_tools(self):
        """Register all MCP tools."""
        
        @self.mcp.tool()
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

        @self.mcp.tool()
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

        @self.mcp.tool()
        async def get_interest_by_region(
            keyword: str,
            resolution: str = "COUNTRY",
            timeframe: str = "today 12-m",
            geo: str = "",
            ctx: Context[ServerSession, None] = None,
        ) -> List[RegionInterest]:
            """
            Get interest by geographic region for a keyword.
            
            Args:
                keyword: Search term to analyze
                resolution: Geographic resolution ('COUNTRY', 'REGION', 'CITY', 'DMA')
                timeframe: Time range for analysis
                geo: Geographic location filter
            
            Returns:
                List of regions with interest values
            """
            if ctx:
                await ctx.info(f"Getting regional interest for: {keyword}")
            
            try:
                data = self.trends_api.get_interest_by_region([keyword], resolution, timeframe, geo)
                
                results = []
                if not data.empty and keyword in data.columns:
                    # Get top 20 regions
                    top_regions = data.nlargest(20, keyword)
                    
                    for region, row in top_regions.iterrows():
                        results.append(RegionInterest(
                            region=region,
                            interest=int(row[keyword]),
                            keyword=keyword
                        ))
                
                if ctx:
                    await ctx.info(f"Found interest data for {len(results)} regions")
                
                return results
                
            except Exception as e:
                if ctx:
                    await ctx.error(f"Error getting regional interest: {str(e)}")
                raise

        @self.mcp.tool()
        async def get_trending_searches(
            geo: str = "US",
            ctx: Context[ServerSession, None] = None,
        ) -> List[str]:
            """
            Get trending searches for a location.
            
            Args:
                geo: Geographic location (e.g., 'US', 'GB', 'CA')
            
            Returns:
                List of trending search terms
            """
            if ctx:
                await ctx.info(f"Getting trending searches for: {geo}")
            
            try:
                trending = self.trends_api.get_trending_searches(geo)
                
                if ctx:
                    await ctx.info(f"Found {len(trending)} trending searches")
                
                return trending[:20]  # Return top 20
                
            except Exception as e:
                if ctx:
                    await ctx.error(f"Error getting trending searches: {str(e)}")
                raise

        @self.mcp.tool()
        async def export_trends_to_csv(
            keywords: List[str],
            timeframe: str = "today 12-m",
            geo: str = "US",
            filename: Optional[str] = None,
            ctx: Context[ServerSession, None] = None,
        ) -> ExportResult:
            """
            Export Google Trends data to CSV file.
            
            Args:
                keywords: List of search terms
                timeframe: Time range for data
                geo: Geographic location
                filename: Optional custom filename
            
            Returns:
                Export result with file details
            """
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

        @self.mcp.tool()
        async def export_trends_to_json(
            keywords: List[str],
            timeframe: str = "today 12-m",
            geo: str = "US",
            filename: Optional[str] = None,
            ctx: Context[ServerSession, None] = None,
        ) -> ExportResult:
            """
            Export Google Trends data to JSON file.
            
            Args:
                keywords: List of search terms
                timeframe: Time range for data
                geo: Geographic location
                filename: Optional custom filename
            
            Returns:
                Export result with file details
            """
            if ctx:
                await ctx.info(f"Exporting trends data to JSON for: {keywords}")
            
            try:
                data = self.trends_api.search_trends(keywords, timeframe, geo)
                
                if data.empty:
                    raise ValueError("No data to export")
                
                # Generate filename
                filename = generate_filename("trends", keywords, "json", filename)
                
                # Create export directory
                export_dir = create_export_directory("google_trends_exports")
                file_path = export_dir / filename
                
                # Convert to JSON-friendly format
                json_data = {
                    "metadata": {
                        "keywords": keywords,
                        "timeframe": timeframe,
                        "geo": geo,
                        "export_date": datetime.now().isoformat(),
                        "data_points": len(data)
                    },
                    "data": data.reset_index().to_dict(orient='records')
                }
                
                # Export data
                with open(file_path, 'w') as f:
                    json.dump(json_data, f, indent=2, default=str)
                
                # Get file size
                size_bytes = file_path.stat().st_size
                
                if ctx:
                    await ctx.info(f"Exported {len(data)} data points to {filename}")
                
                return ExportResult(
                    filename=filename,
                    format="json",
                    size_bytes=size_bytes,
                    path=str(file_path)
                )
                
            except Exception as e:
                if ctx:
                    await ctx.error(f"Error exporting to JSON: {str(e)}")
                raise

        @self.mcp.tool()
        async def create_sql_table(
            keywords: List[str],
            timeframe: str = "today 12-m",
            geo: str = "US",
            table_name: Optional[str] = None,
            ctx: Context[ServerSession, None] = None,
        ) -> SQLTableResult:
            """
            Create SQLite table with Google Trends data.
            
            Args:
                keywords: List of search terms
                timeframe: Time range for data
                geo: Geographic location
                table_name: Optional custom table name
            
            Returns:
                SQL table creation result
            """
            if ctx:
                await ctx.info(f"Creating SQL table for: {keywords}")
            
            try:
                data = self.trends_api.search_trends(keywords, timeframe, geo)
                
                if data.empty:
                    raise ValueError("No data to create table from")
                
                # Generate table name
                if not table_name:
                    keyword_str = "_".join(keywords[:3]).replace(" ", "_").lower()
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    table_name = f"trends_{keyword_str}_{timestamp}"
                
                # Sanitize table name
                table_name = sanitize_table_name(table_name)
                
                # Create database directory
                db_dir = create_export_directory("google_trends_db")
                db_path = db_dir / f"{table_name}.db"
                
                # Create SQLite database and table
                conn = sqlite3.connect(str(db_path))
                
                # Reset index to make date a regular column
                data_reset = data.reset_index()
                data_reset.rename(columns={'date': 'trend_date'}, inplace=True)
                
                # Write to SQLite
                data_reset.to_sql(table_name, conn, if_exists='replace', index=False)
                
                # Get table info
                cursor = conn.cursor()
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [row[1] for row in cursor.fetchall()]
                
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                row_count = cursor.fetchone()[0]
                
                conn.close()
                
                if ctx:
                    await ctx.info(f"Created SQL table '{table_name}' with {row_count} rows")
                
                return SQLTableResult(
                    table_name=table_name,
                    rows_inserted=row_count,
                    columns=columns,
                    database_path=str(db_path)
                )
                
            except Exception as e:
                if ctx:
                    await ctx.error(f"Error creating SQL table: {str(e)}")
                raise

        @self.mcp.tool()
        async def get_available_timeframes(ctx: Context[ServerSession, None] = None) -> List[str]:
            """
            Get list of available timeframes for Google Trends queries.
            
            Returns:
                List of available timeframe options
            """
            if ctx:
                await ctx.info(f"Available timeframes: {len(AVAILABLE_TIMEFRAMES)} options")
            
            return AVAILABLE_TIMEFRAMES

        @self.mcp.tool()
        async def get_available_regions(ctx: Context[ServerSession, None] = None) -> List[str]:
            """
            Get list of available geographic regions.
            
            Returns:
                List of available region codes
            """
            if ctx:
                await ctx.info(f"Available regions: {len(AVAILABLE_REGIONS)} countries")
            
            return AVAILABLE_REGIONS

        @self.mcp.tool()
        async def compare_keywords_comprehensive(
            keywords: List[str],
            timeframe: str = "today 12-m",
            geo: str = "US",
            ctx: Context[ServerSession, None] = None,
        ) -> ComparisonResult:
            """
            Comprehensive comparison of multiple keywords including trends, related queries, and regional interest.
            
            Args:
                keywords: List of keywords to compare
                timeframe: Time range for analysis
                geo: Geographic location
            
            Returns:
                Comprehensive comparison data
            """
            if ctx:
                await ctx.info(f"Starting comprehensive comparison of: {keywords}")
            
            try:
                # Get trends data
                trends_data = await search_trends(keywords, timeframe, geo, ctx)
                
                # Get related queries for each keyword
                related_queries = {}
                for keyword in keywords:
                    try:
                        related = await get_related_queries(keyword, timeframe, geo, ctx)
                        related_queries[keyword] = related
                    except Exception as e:
                        if ctx:
                            await ctx.warning(f"Could not get related queries for {keyword}: {str(e)}")
                        related_queries[keyword] = []
                
                # Get regional interest for first keyword
                regional_interest = []
                if keywords:
                    try:
                        regional_interest = await get_interest_by_region(keywords[0], "COUNTRY", timeframe, geo, ctx)
                    except Exception as e:
                        if ctx:
                            await ctx.warning(f"Could not get regional interest: {str(e)}")
                
                # Compile results
                result = ComparisonResult(
                    keywords=keywords,
                    timeframe=timeframe,
                    geo=geo,
                    analysis_date=datetime.now().isoformat(),
                    trends_data=trends_data,
                    related_queries=related_queries,
                    regional_interest=regional_interest,
                    summary={
                        "total_keywords": len(keywords),
                        "total_trend_points": len(trends_data),
                        "total_related_queries": sum(len(v) for v in related_queries.values()),
                        "total_regions": len(regional_interest)
                    }
                )
                
                if ctx:
                    await ctx.info(f"Completed comprehensive comparison with {result.summary['total_trend_points']} trend points")
                
                return result
                
            except Exception as e:
                if ctx:
                    await ctx.error(f"Error in comprehensive comparison: {str(e)}")
                raise

    def initialize_api(self):
        """Initialize the Google Trends API instance."""
        if self.trends_api is None:
            self.trends_api = GoogleTrendsAPI()
            print("Google Trends API initialized successfully")

    def run(self):
        """Run the MCP server."""
        self.initialize_api()
        self.mcp.run()
