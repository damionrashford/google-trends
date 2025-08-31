# Google Trends MCP Server

A Model Context Protocol (MCP) server that provides access to Google Trends data for search trend analysis, related queries, geographic interest, and data export capabilities.

## 🚀 Quick Start

```bash
# Clone and setup
git clone <repository-url>
cd google-trends

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
```

## 📦 Features

- **Trend Analysis**: Search and analyze Google Trends data
- **Related Queries**: Get top and rising related search queries
- **Geographic Interest**: Analyze regional interest patterns
- **Data Export**: Export to CSV, JSON, or SQLite databases
- **Rate Limiting**: Built-in rate limiting and retry logic

## 🏗️ Project Structure

```
google-trends/
├── src/google_trends_mcp/     # Main package
│   ├── api/                   # API components
│   ├── models/                # Data models
│   ├── server/                # MCP server
│   └── utils/                 # Utilities
├── tests/                     # Test suite
├── docs/                      # Documentation
├── main.py                    # Entry point
└── requirements.txt           # Dependencies
```

## 🔧 Usage

### Running the Server
```bash
# Method 1: Using main.py
python main.py

# Method 2: Using the package
python -m src.google_trends_mcp
```

### Available MCP Tools

1. `search_trends` - Search for Google Trends data
2. `get_related_queries` - Get related search queries
3. `get_interest_by_region` - Get geographic interest data
4. `get_trending_searches` - Get trending searches
5. `export_trends_to_csv` - Export data to CSV
6. `export_trends_to_json` - Export data to JSON
7. `create_sql_table` - Create SQLite database
8. `get_available_timeframes` - List available timeframes
9. `get_available_regions` - List available regions
10. `compare_keywords_comprehensive` - Comprehensive keyword comparison

## ⚙️ Configuration

### Timeframes
- `now 1-H` to `2004-present`

### Regions
- US, GB, CA, AU, DE, FR, IT, ES, NL, BR, and 20+ more

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=src/google_trends_mcp tests/
```

## 📝 Development

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

## ⚠️ Disclaimer

This project uses the unofficial Google Trends API through the `pytrends` library. Google may rate-limit or block requests. The server includes built-in retry logic and rate limiting to handle these issues gracefully.

## 📄 License

MIT License

---

**Built with ❤️ for the MCP community**
