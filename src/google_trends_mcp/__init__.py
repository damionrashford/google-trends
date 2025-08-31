"""
Google Trends MCP Server Package
A comprehensive Model Context Protocol server for Google Trends data
"""

__version__ = "1.0.0"
__author__ = "Google Trends MCP Team"
__description__ = "A comprehensive Google Trends API server that provides access to search trend data, related queries, geographic interest, and data export capabilities."

from .server import GoogleTrendsMCPServer

__all__ = ["GoogleTrendsMCPServer"]
