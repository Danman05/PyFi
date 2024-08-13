import yfinance as yf
import ta
import requests
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor

# Define parameters for your strategy

THRESHOLDS = {
    "pe_ratio_threshold": 20, # Stocks with a P/E ratio below this are considered undervalued.
    "rsi_threshold": 30, # RSI below 30 indicates oversold conditions.
    "current_ratio_threshold": 1, # Current Ratio above 1.5 is usually seen as a good sign of liquidity.
    "quick_ratio_threshold": 1, # Quick Ratio above 1.0 is generally considered a good indicator of financial health.
    "roe_threshold": 0,
    "gross_margin_threshold": 0
}

# Create a list to store potential buying opportunities
buying_opportunities = []

def fetch_symbol_data(ticker='AAPL', period='ytd'):
    symbol = yf.Ticker(ticker)
    return symbol.history(period=period)

def fetch_stock_info(symbol):
    stock = yf.Ticker(symbol)
    return stock.info

def check_financial_health(latest_data):
    try:
        # Extract financial data
        pe_ratio = latest_data.get('forwardPE', None)
        current_ratio = latest_data.get('currentRatio', None)
        quick_ratio = latest_data.get('quickRatio', None)
        roe = latest_data.get('returnOnEquity', None)
        gross_margin = latest_data.get('grossMargins', None)

        # Check missing values
        if None in [pe_ratio, current_ratio, quick_ratio, roe, gross_margin]:
            missing_data = [key for key, value in locals().items() if value is None]
            return None, f"Missing essential financial data: {', '.join(missing_data)}"

        # Ensure the values are valid numbers
        financials = {
            "pe_ratio": float(pe_ratio),
            "current_ratio": float(current_ratio),
            "quick_ratio": float(quick_ratio),
            "roe": float(roe),
            "gross_margin": float(gross_margin)
        }

        return financials, None
    except (ValueError, TypeError) as e:
        return None, f"Error processing financial data: {e}"
    

def evaluate_stock(symbol, data, latest_data):
    financials, error = check_financial_health(latest_data)
    if error:
        print(f"{symbol}: {error}")
        return None

    # Calculate RSI
    data['RSI'] = ta.momentum.RSIIndicator(data['Close']).rsi()
    latest_rsi = data['RSI'].iloc[-1] if not data['RSI'].empty else None

    if latest_rsi is None:
        print(f"{symbol}: RSI data is missing or incomplete.")
        return None

    # Apply thresholds to determine potential buying opportunity
    if (financials["pe_ratio"] < THRESHOLDS["pe_ratio_threshold"] and
        financials["current_ratio"] > THRESHOLDS["current_ratio_threshold"] and
        financials["quick_ratio"] > THRESHOLDS["quick_ratio_threshold"] and
        financials["roe"] > THRESHOLDS["roe_threshold"] and
        financials["gross_margin"] > THRESHOLDS["gross_margin_threshold"]):
        data = ({
            'Symbol': symbol,
            'PE Ratio': financials["pe_ratio"],
            'RSI': latest_rsi,
            'Current Ratio': financials["current_ratio"],
            'Quick Ratio': financials["quick_ratio"],
            'ROE': financials["roe"],
            'Gross Margin': financials["gross_margin"],
            'Market Cap': latest_data.get('marketCap', None)
        })
        buying_opportunities.append(data)

        return True

    return False

def check_stock(symbol):
    try:
        data = fetch_symbol_data(symbol)
        if data.empty:
            return f"No historical data found for {symbol} | Not older than a year."

        latest_data = fetch_stock_info(symbol)
        if evaluate_stock(symbol, data, latest_data):
            print(f'New opportunity: {symbol}')
        return None
    except Exception as e:
        print(f"Error checking {symbol}: {e}")
        return f"Error checking {symbol}: {e}"

def fetch_symbols(scan_location='america'):

    if scan_location == 'debug':
        symbols =( 'DEBUG:GME', 'DEBUG:MOFG', 'DEBUG:HOFV', 'DEBUG:JCSE', 'DEBUG:STRR', 'DEBUG:UONE', 'DEBUG:DJCO', 'DEBUG:MCAGU', 'DEBUG:DSY', 'DEBUG:SLDP',
        'DEBUG:OXSQ', 'DEBUG:RRR', 'DEBUG:VRA', 'DEBUG:YHGJ', 'DEBUG:COLL', 'DEBUG:FSHPU', 'DEBUG:JTEK', 'DEBUG:FIVN', 'DEBUG:TBRG', 'DEBUG:RPD', 'DEBUG:BTCT',
        'DEBUG:BHRB', 'DEBUG:LBTYK', 'DEBUG:RFAIU', 'DEBUG:RFAC', 'DEBUG:CEAD', 'DEBUG:POOL', 'DEBUG:SRBK', 'DEBUG:ON', 'DEBUG:KELYB', 'DEBUG:MTSI', 'DEBUG:FCA',
        'DEBUG:ESEA', 'DEBUG:STSS', 'DEBUG:XP', 'DEBUG:NVMI', 'DEBUG:SOGP', 'DEBUG:FRST', 'DEBUG:ARCC', 'DEBUG:MVST', 'DEBUG:RKLB', 'DEBUG:TMC', 'DEBUG:BBSI',
        'DEBUG:GLSI', 'DEBUG:INOD', 'DEBUG:AMLI', 'DEBUG:NMTC', 'DEBUG:RNAC', 'DEBUG:NUTX', 'DEBUG:ULH', 'DEBUG:NTNX', 'DEBUG:ULCC', 'DEBUG:CSF', 'DEBUG:SMCI',
        'DEBUG:PSCD', 'DEBUG:SHPH', 'DEBUG:PLMI', 'DEBUG:INBX', 'DEBUG:IBIT', 'DEBUG:BANX', 'DEBUG:CAMT', 'DEBUG:HUBC', 'DEBUG:PSCF', 'DEBUG:BGXX', 'DEBUG:IART',
        'DEBUG:TXG', 'DEBUG:AGNCP', 'DEBUG:MNTL', 'DEBUG:PRLD', 'DEBUG:ALLR', 'DEBUG:CDTG', 'DEBUG:PDBC', 'DEBUG:PLAB', 'DEBUG:KZR', 'DEBUG:SAFT', 'DEBUG:SOWG',
        'DEBUG:SLS', 'DEBUG:AFBI', 'DEBUG:MGRM', 'DEBUG:CCNE', 'DEBUG:CRBU', 'DEBUG:PCSA', 'DEBUG:ROP', 'DEBUG:LFVN', 'DEBUG:COLM', 'DEBUG:AEYE', 'DEBUG:PFM', 'DEBUG:UNB')
        return [{"exchange": i.split(":")[0], "ticker": i.split(":")[1]} for i in symbols]

    try:
        url = f'https://scanner.tradingview.com/{scan_location}/scan'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        symbols = [item["s"] for item in data.get("data", [])]
        return [{"exchange": i.split(":")[0], "ticker": i.split(":")[1]} for i in symbols]
    except requests.RequestException as e:
        print(f"Error fetching symbols: {e}")
        return []

def get_symbols(scan_location='america', symbols=None):
    if not symbols:
        symbols = fetch_symbols(scan_location)
    return [s["ticker"] for s in symbols]

def get_symbols_by_exchange(scan_location='america', exchange='NASDAQ', symbols=None):
    if not symbols:
        symbols = fetch_symbols(scan_location)
    return [s["ticker"] for s in symbols if s["exchange"] == exchange]

def scan_symbols(symbols=None, workers=10, exchange= 'NASDAQ', scan_location='america'):
    global buying_opportunities
    buying_opportunities = []
    if not symbols:
        symbols = get_symbols_by_exchange(scan_location=scan_location, exchange=exchange)
    
    with ThreadPoolExecutor(max_workers=workers) as executor:
        {executor.submit(check_stock, s): s for s in np.sort(symbols) if '/' not in s and '.' not in s}


def get_count_of_filtered_symbols(scan_location, exchange):
    return len([s for s in get_symbols_by_exchange(scan_location, exchange) if '/' not in s and '.' not in s] )

def save_opportunities_to_csv(file_path='buying_opportunities.csv'):
    opportunities_df = pd.DataFrame(buying_opportunities)
    opportunities_df.to_csv(file_path, index=False)
    opportunities_df.to_csv("Debug_CSV.csv", index=False)


# financial_data = (
#     f"Symbol {symbol:>20}\n"
#     f"PE Ratio: {round(pe_ratio, 2):>18} {'✅' if bool_pe_ratio else '❌':>5}\n"
#     f"Current Ratio: {round(current_ratio, 2):>10} {'✅' if bool_current_ratio else '❌':>5}\n"
#     f"Quick Ratio: {round(quick_ratio, 2):>12} {'✅' if bool_quick_ratio else '❌':>5}\n"
#     f"ROE: {round(roe, 2):>26} {'✅' if bool_roe else '❌':>5}\n"
#     f"Gross Margin: {round(gross_margin, 2):>9} {'✅' if bool_gross_margin else '❌':>5}\n"
#     f"\nIndicators\n"
#     f"RSI: {round(latest_rsi, 2):>28}"
# )

# ticker = 'GME'
# check_stock(ticker)