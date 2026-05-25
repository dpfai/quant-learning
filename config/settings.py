"""
Project configuration settings.
"""

# Default tickers for market overview.
DEFAULT_TICKERS = ["SPY", "QQQ", "DIA", "IWM", "VIX"]

# Data settings.
DATA_CACHE_DIR = "data/cache"
DATA_RAW_DIR = "data/raw"
DATA_PROCESSED_DIR = "data/processed"
DEFAULT_PERIOD = "2y"
CACHE_MAX_AGE_HOURS = 24
CACHE_FILE_FORMAT = "{ticker}_{period}.parquet"
TICKER_ALIASES = {
    "VIX": "^VIX",
}

# Chart settings.
DEFAULT_CHART_HEIGHT = 600
