# Google Trends MCP Server - Component Architecture

## Overview

The Google Trends MCP Server has been refactored into a properly componentized architecture with clear separation of concerns, modular design, and focused responsibilities.

## 🏗️ Component Architecture

### 1. API Layer (`src/google_trends_mcp/api/`)

#### `RateLimiter` Component
- **Purpose**: Handles rate limiting and retry logic
- **Responsibilities**:
  - Exponential backoff for failed requests
  - Request delay management
  - Error handling and retry logic
- **Key Methods**:
  - `wait_for_rate_limit()`: Manages delays between requests
  - `retry_with_backoff()`: Implements exponential backoff
  - `_get_empty_result()`: Returns appropriate empty results

#### `TrendsClient` Component
- **Purpose**: Core Google Trends API interactions
- **Responsibilities**:
  - Direct API communication with pytrends
  - Request building and payload management
  - Basic data fetching operations
- **Key Methods**:
  - `search_trends()`: Fetch trend data
  - `get_related_queries()`: Get related search queries
  - `get_interest_by_region()`: Get geographic interest data
  - `get_trending_searches()`: Get trending searches

#### `DataAnalyzer` Component
- **Purpose**: Data analysis and statistics
- **Responsibilities**:
  - Statistical calculations
  - Trend analysis
  - Keyword comparisons
  - Seasonal pattern detection
- **Key Methods**:
  - `get_statistics()`: Comprehensive statistics
  - `compare_keywords()`: Multi-keyword analysis
  - `get_seasonal_patterns()`: Seasonal pattern analysis
  - `_calculate_trend_direction()`: Trend direction calculation

#### `GoogleTrendsAPI` Component (Main API)
- **Purpose**: High-level API interface
- **Responsibilities**:
  - Orchestrates other components
  - Provides unified interface
  - Maintains backward compatibility
- **Dependencies**:
  - `TrendsClient` for API calls
  - `DataAnalyzer` for analysis
  - `RateLimiter` for request management

### 2. Server Layer (`src/google_trends_mcp/server/`)

#### `ToolRegistry` Component
- **Purpose**: Manages MCP tool registration
- **Responsibilities**:
  - Tool registration and organization
  - Tool lookup and management
  - Tool counting and listing
- **Key Methods**:
  - `register_tool()`: Register new tools
  - `get_tool()`: Retrieve tools by name
  - `list_tools()`: List all registered tools
  - `get_tool_count()`: Count registered tools

#### `ToolFactory` Component
- **Purpose**: Creates and configures MCP tools
- **Responsibilities**:
  - Tool creation with proper dependencies
  - Tool configuration and setup
  - Dependency injection
- **Key Methods**:
  - `create_search_trends_tool()`: Create trends search tool
  - `create_related_queries_tool()`: Create related queries tool
  - `create_export_tools()`: Create export tools
  - `create_utility_tools()`: Create utility tools

#### `GoogleTrendsMCPServer` Component (Main Server)
- **Purpose**: Main MCP server implementation
- **Responsibilities**:
  - Server initialization and management
  - Component orchestration
  - Tool registration coordination
- **Dependencies**:
  - `ToolRegistry` for tool management
  - `ToolFactory` for tool creation
  - `GoogleTrendsAPI` for data access

### 3. Models Layer (`src/google_trends_mcp/models/`)

#### `schemas.py` - Pydantic Models
- **Purpose**: Structured data models
- **Components**:
  - `TrendData`: Trend analysis results
  - `RelatedQuery`: Related search queries
  - `RegionInterest`: Geographic interest data
  - `ExportResult`: Export operation results
  - `SQLTableResult`: Database operation results
  - `ComparisonResult`: Comprehensive comparison data

### 4. Utils Layer (`src/google_trends_mcp/utils/`)

#### `constants.py` - Configuration Constants
- **Purpose**: System constants and configuration
- **Components**:
  - `AVAILABLE_TIMEFRAMES`: Supported time ranges
  - `AVAILABLE_REGIONS`: Supported geographic regions
  - Default values and settings

#### `helpers.py` - Utility Functions
- **Purpose**: Shared utility functions
- **Components**:
  - `generate_filename()`: File naming utilities
  - `create_export_directory()`: Directory management
  - `sanitize_table_name()`: SQL table name sanitization
  - `format_date_range()`: Date formatting utilities

## 🔄 Data Flow

```
MCP Client Request
    ↓
GoogleTrendsMCPServer
    ↓
ToolRegistry → ToolFactory
    ↓
GoogleTrendsAPI
    ↓
TrendsClient + RateLimiter
    ↓
Google Trends API (pytrends)
    ↓
DataAnalyzer (for processing)
    ↓
Pydantic Models (for structure)
    ↓
Structured Response
```

## 🎯 Benefits of Componentization

### 1. **Single Responsibility Principle**
- Each component has one clear purpose
- Easy to understand and maintain
- Reduced complexity per component

### 2. **Dependency Injection**
- Components are loosely coupled
- Easy to test individual components
- Flexible configuration

### 3. **Reusability**
- Components can be used independently
- Easy to extend with new functionality
- Modular design promotes reuse

### 4. **Testability**
- Each component can be tested in isolation
- Mock dependencies easily
- Better test coverage

### 5. **Maintainability**
- Clear separation of concerns
- Easy to locate and fix issues
- Simple to add new features

### 6. **Scalability**
- Components can be scaled independently
- Easy to add new components
- Flexible architecture

## 🔧 Adding New Components

### 1. **New API Component**
```python
# src/google_trends_mcp/api/new_component.py
class NewComponent:
    def __init__(self):
        pass
    
    def new_method(self):
        pass
```

### 2. **Update API Init**
```python
# src/google_trends_mcp/api/__init__.py
from .new_component import NewComponent

__all__ = [
    "GoogleTrendsAPI",
    "NewComponent"
]
```

### 3. **Integrate with Main API**
```python
# src/google_trends_mcp/api/trends_api.py
from .new_component import NewComponent

class GoogleTrendsAPI:
    def __init__(self):
        self.new_component = NewComponent()
```

## 🧪 Testing Components

### 1. **Unit Testing**
```python
# tests/test_new_component.py
def test_new_component():
    component = NewComponent()
    result = component.new_method()
    assert result is not None
```

### 2. **Integration Testing**
```python
# tests/test_integration.py
def test_component_integration():
    api = GoogleTrendsAPI()
    result = api.new_method()
    assert result is not None
```

## 📊 Component Metrics

- **Total Components**: 8 focused components
- **Lines of Code per Component**: 50-200 lines
- **Dependencies per Component**: 1-3 dependencies
- **Test Coverage**: Each component independently testable

## 🚀 Future Enhancements

1. **Plugin System**: Allow external components
2. **Configuration Management**: Centralized configuration
3. **Logging Framework**: Structured logging per component
4. **Performance Monitoring**: Component-level metrics
5. **Caching Layer**: Component-specific caching

This componentized architecture provides a solid foundation for a maintainable, scalable, and testable Google Trends MCP Server.
