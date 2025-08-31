# Google Trends MCP Server - Architecture

## Overview

The Google Trends MCP Server is built using a modular, component-based architecture that separates concerns and promotes maintainability.

## Architecture Components

### 1. Package Structure (`src/google_trends_mcp/`)

```
google_trends_mcp/
├── __init__.py              # Package initialization and exports
├── __main__.py              # Entry point for direct execution
├── api/                     # Core API functionality
│   ├── __init__.py
│   └── trends_api.py        # Google Trends API wrapper
├── models/                  # Data models and schemas
│   ├── __init__.py
│   └── schemas.py           # Pydantic models
├── server/                  # MCP server implementation
│   ├── __init__.py
│   └── mcp_server.py        # Main server class
└── utils/                   # Utilities and helpers
    ├── __init__.py
    ├── constants.py         # Constants and configuration
    └── helpers.py           # Helper functions
```

### 2. Core Components

#### API Layer (`api/`)
- **Purpose**: Encapsulates Google Trends API interactions
- **Key Class**: `GoogleTrendsAPI`
- **Features**: 
  - Rate limiting and retry logic
  - Error handling
  - Data transformation

#### Models Layer (`models/`)
- **Purpose**: Defines structured data models
- **Key Classes**: 
  - `TrendData`: Trend analysis results
  - `RelatedQuery`: Related search queries
  - `RegionInterest`: Geographic interest data
  - `ExportResult`: Export operation results
  - `SQLTableResult`: Database operation results
  - `ComparisonResult`: Comprehensive comparison data

#### Server Layer (`server/`)
- **Purpose**: MCP server implementation
- **Key Class**: `GoogleTrendsMCPServer`
- **Features**:
  - Tool registration
  - Request handling
  - Response formatting

#### Utils Layer (`utils/`)
- **Purpose**: Shared utilities and constants
- **Components**:
  - `constants.py`: Available timeframes and regions
  - `helpers.py`: File operations and data processing

### 3. Data Flow

```
Client Request → MCP Server → API Layer → Google Trends → Response Processing → Structured Output
```

1. **Client Request**: MCP client sends tool request
2. **MCP Server**: Routes request to appropriate tool
3. **API Layer**: Interacts with Google Trends API
4. **Google Trends**: Returns raw data
5. **Response Processing**: Transforms data using Pydantic models
6. **Structured Output**: Returns formatted response

### 4. Error Handling

- **Rate Limiting**: Exponential backoff with retries
- **API Errors**: Graceful degradation with fallback data
- **Validation**: Pydantic model validation
- **Logging**: Context-aware logging for debugging

### 5. Configuration

- **Timeframes**: 9 predefined time ranges
- **Regions**: 30 supported geographic locations
- **Rate Limiting**: Configurable delays and retries
- **Export Paths**: Temporary directory management

### 6. Extensibility

The architecture supports easy extension:

1. **New API Methods**: Add to `api/trends_api.py`
2. **New Data Models**: Add to `models/schemas.py`
3. **New Tools**: Register in `server/mcp_server.py`
4. **New Utilities**: Add to `utils/` directory

### 7. Testing Strategy

- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end workflow testing
- **Mock Testing**: API response simulation
- **Error Testing**: Edge case and failure scenarios

## Benefits of This Architecture

1. **Modularity**: Clear separation of concerns
2. **Maintainability**: Easy to modify and extend
3. **Testability**: Isolated components for testing
4. **Reusability**: Shared utilities and models
5. **Scalability**: Easy to add new features
6. **Reliability**: Robust error handling and rate limiting
