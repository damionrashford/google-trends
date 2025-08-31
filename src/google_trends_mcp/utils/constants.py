"""
Constants for Google Trends MCP Server
Available timeframes and geographic regions
"""

# Available timeframes for Google Trends queries
AVAILABLE_TIMEFRAMES = [
    'now 1-H',    # Past hour
    'now 4-H',    # Past 4 hours
    'now 1-d',    # Past day
    'now 7-d',    # Past 7 days
    'today 1-m',  # Past month
    'today 3-m',  # Past 3 months
    'today 12-m', # Past 12 months
    'today 5-y',  # Past 5 years
    '2004-present' # All time
]

# Available geographic regions
AVAILABLE_REGIONS = [
    'US', 'GB', 'CA', 'AU', 'DE', 'FR', 'IT', 'ES', 'NL', 'BR',
    'MX', 'AR', 'CL', 'CO', 'PE', 'VE', 'JP', 'KR', 'IN', 'SG',
    'MY', 'TH', 'VN', 'PH', 'ID', 'NZ', 'ZA', 'EG', 'NG', 'KE'
]

# Default values
DEFAULT_TIMEFRAME = 'today 12-m'
DEFAULT_GEO = 'US'
DEFAULT_RESOLUTION = 'COUNTRY'

# Rate limiting settings
DEFAULT_REQUEST_DELAY = 5.0
DEFAULT_MAX_RETRIES = 5
DEFAULT_BASE_DELAY = 10.0
