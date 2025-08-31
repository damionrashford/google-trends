"""
Data Models Module
Pydantic models for structured data output
"""

from .schemas import (
    TrendData,
    RelatedQuery,
    RegionInterest,
    ExportResult,
    SQLTableResult,
    ComparisonResult
)

__all__ = [
    "TrendData",
    "RelatedQuery", 
    "RegionInterest",
    "ExportResult",
    "SQLTableResult",
    "ComparisonResult"
]
