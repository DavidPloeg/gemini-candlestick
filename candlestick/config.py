"""Settings shared across the app."""

# Folders for generated output
DATA_DIRECTORIES = [
    'data/pdf',            # PDF reports
    'data/csv',            # CSV data files
    'data/png',            # PNG chart images
    'data/png_optimized',  # Optimized PNG chart images (uploaded to Gemini and Telegram)
    'data/txt',            # Text files
]

# Chart layout
CANDLESTICK_CHART_NO = 26 * 7  # Number of trading days shown on each chart
FUTURE_CLOUD_NO = 26 * 1       # Number of days the Ichimoku Cloud is projected ahead
GRAPH_WIDTH = {
    '1d': 0.75,  # Candlestick and volume bar width for the daily interval
}

# Gemini
DEFAULT_GEMINI_MODEL = "gemini-3.8-flash"

# Telegram
MAX_MEDIA_GROUP_SIZE = 8  # Images sent per Telegram album

# Market sectors, see prompts.sector_text()
SECTOR_LIST = [
    'Renewable Energy',
    'Biotechnology',
    'Information Technology',
    'Health Care',
    'Materials',
    'Industrials',
    'Consumer Discretionary',
    'Consumer Staples',
    'Communication Services',
    'Utilities',
    'Transportation',
    'Energy',
    'Financials',
    'Real Estate',
    'Hospitality'
]
