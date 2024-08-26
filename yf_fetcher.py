import yfinance as yf

def fetch_ticker(ticker: str):
    """
    Creates ticker object. - Does not make a network request

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
         Ticker
    """
    try:
        ticker_data = yf.Ticker(ticker)
        return ticker_data
    except Exception as e:
        raise ValueError(f"Failed to fetch data for ticker {ticker}: {e}")

def fetch_ticker_history(ticker, period = 'ytd'):
    """
    Fetches ticker history using yfinance.

    Args:
        ticker (str): The stock ticker symbol.
        period (str): The period for which to fetch historical data.

    Returns:
        DataFrame: Ticker history data.
    """
    try:
        ticker_data = yf.Ticker(ticker)
        return ticker_data.history(period)
    except Exception as e:
        raise ValueError(f"Failed to fetch historical data for ticker {ticker}: {e}")

def fetch_ticker_info(ticker):
    """
    Fetches ticker info using yfinance.

    Args:
        ticker (str): The stock ticker symbol.

    Returns:
        dict: Ticker information.
    """
    try:
        ticker_data = yf.Ticker(ticker)
        return ticker_data.info
    except Exception as e:
        raise ValueError(f"Failed to fetch data for ticker {ticker}: {e}")
