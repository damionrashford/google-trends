#!/usr/bin/env python3
"""
Google Trends MCP Server Entry Point
Run the MCP server directly
"""

from .server import GoogleTrendsMCPServer


def main():
    """Main entry point for the Google Trends MCP Server."""
    server = GoogleTrendsMCPServer()
    server.run()


if __name__ == "__main__":
    main()
