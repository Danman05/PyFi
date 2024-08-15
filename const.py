_ALLOWED_PERIODS_ =  ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', 'ytd', 'max']

_EVALUTATION_THRESHOLDS_ = {
    "pe_ratio_threshold": 20, # Stocks with a P/E ratio below this are considered undervalued.
    "rsi_threshold": 30, # RSI below 30 indicates oversold conditions.
    "current_ratio_threshold": 1, # Current Ratio above 1.5 is usually seen as a good sign of liquidity.
    "quick_ratio_threshold": 1, # Quick Ratio above 1.0 is generally considered a good indicator of financial health.
    "roe_threshold": 0,
    "gross_margin_threshold": 0
}