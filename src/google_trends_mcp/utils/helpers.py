"""
Helper functions for Google Trends MCP Server
Utility functions for file operations and data processing
"""

import tempfile
from datetime import datetime
from pathlib import Path
from typing import List, Optional


def generate_filename(prefix: str, keywords: List[str], extension: str, 
                     custom_name: Optional[str] = None) -> str:
    """
    Generate a filename for export operations.
    
    Args:
        prefix: File prefix (e.g., 'trends', 'export')
        keywords: List of keywords
        extension: File extension (e.g., 'csv', 'json')
        custom_name: Optional custom filename
        
    Returns:
        Generated filename
    """
    if custom_name:
        if not custom_name.endswith(f'.{extension}'):
            custom_name += f'.{extension}'
        return custom_name
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    keyword_str = "_".join(keywords[:3])  # Use first 3 keywords
    return f"{prefix}_{keyword_str}_{timestamp}.{extension}"


def create_export_directory(directory_name: str) -> Path:
    """
    Create export directory in temp folder.
    
    Args:
        directory_name: Name of the export directory
        
    Returns:
        Path to created directory
    """
    export_dir = Path(tempfile.gettempdir()) / directory_name
    export_dir.mkdir(exist_ok=True)
    return export_dir


def sanitize_table_name(name: str) -> str:
    """
    Sanitize table name for SQLite compatibility.
    
    Args:
        name: Original table name
        
    Returns:
        Sanitized table name
    """
    # Remove or replace invalid characters
    sanitized = "".join(c for c in name if c.isalnum() or c == '_')
    
    # Ensure it doesn't start with a digit
    if sanitized and sanitized[0].isdigit():
        sanitized = "t_" + sanitized
    
    return sanitized or "trends_table"


def format_date_range(start_date, end_date) -> str:
    """
    Format date range for display.
    
    Args:
        start_date: Start date
        end_date: End date
        
    Returns:
        Formatted date range string
    """
    return f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
