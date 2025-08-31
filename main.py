#!/usr/bin/env python3
"""
Google Trends MCP Server - Main Entry Point
A comprehensive Model Context Protocol server for Google Trends data
"""

import sys
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from google_trends_mcp.server import GoogleTrendsMCPServer


def main():
    """Main entry point for the Google Trends MCP Server."""
    print("Starting Google Trends MCP Server...")
    server = GoogleTrendsMCPServer()
    server.run()


if __name__ == "__main__":
    main()
