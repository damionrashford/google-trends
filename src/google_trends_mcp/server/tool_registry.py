"""
Tool Registry Component
Manages registration and organization of MCP tools
"""

from typing import Dict, Any, Callable
from mcp.server.fastmcp import FastMCP


class ToolRegistry:
    """Manages registration and organization of MCP tools."""
    
    def __init__(self, mcp_server: FastMCP):
        """
        Initialize the tool registry.
        
        Args:
            mcp_server: FastMCP server instance
        """
        self.mcp_server = mcp_server
        self.registered_tools: Dict[str, Callable] = {}
    
    def register_tool(self, tool_func: Callable) -> Callable:
        """
        Register a tool with the MCP server.
        
        Args:
            tool_func: Tool function to register
            
        Returns:
            Registered tool function
        """
        # Register with FastMCP
        registered_tool = self.mcp_server.tool()(tool_func)
        
        # Store in registry
        self.registered_tools[tool_func.__name__] = registered_tool
        
        return registered_tool
    
    def get_tool(self, tool_name: str) -> Callable:
        """
        Get a registered tool by name.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            Tool function
        """
        return self.registered_tools.get(tool_name)
    
    def list_tools(self) -> list:
        """
        List all registered tools.
        
        Returns:
            List of tool names
        """
        return list(self.registered_tools.keys())
    
    def get_tool_count(self) -> int:
        """
        Get the number of registered tools.
        
        Returns:
            Number of registered tools
        """
        return len(self.registered_tools)
