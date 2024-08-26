_ALLOWED_PERIODS_ =  ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', 'ytd', 'max']

_EVALUATION_THRESHOLDS_ = {
    "forward_pe_threshold": 20, # Stocks with a P/E ratio below this are considered undervalued.
    "rsi_threshold": 30, # RSI below 30 indicates oversold conditions.
    "current_ratio_threshold": 1, # Current Ratio above 1.5 is usually seen as a good sign of liquidity.
    "quick_ratio_threshold": 1, # Quick Ratio above 1.0 is generally considered a good indicator of financial health.
    "roe_threshold": 0,
    "gross_margin_threshold": 0
}

_REQUIRED_DATA = { # Add the required data that needs to be included
    'forwardPE',
    'currentRatio',
    'quickRatio',
    'returnOnEquity',
    'grossMargins',
}

# Define options for locations and exchanges
_SYMBOL_LOCATIONS_ = ["Debug", "America"]

_SYMBOL_EXCHANGES_ = {
    "Debug": ["DEBUG"],
    "America": ["NASDAQ", "NYSE"],
}