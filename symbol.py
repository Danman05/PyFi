import yfinance as yf
import ta
import requests
import json


# Define parameters for your strategy

thresholds = {
    "pe_ratio_threshold": 20, # Stocks with a P/E ratio below this are considered undervalued.
    "rsi_threshold": 30, # RSI below 30 indicates oversold conditions.
    "current_ratio_threshold": 1, # Current Ratio above 1.5 is usually seen as a good sign of liquidity.
    "quick_ratio_threshold": 1, # Quick Ratio above 1.0 is generally considered a good indicator of financial health.
    "roe_threshold": 0,
    "gross_margin_threshold": 0
}

# Create a list to store potential buying opportunities
buying_opportunities = []

def symbol_data(ticker = 'AAPL', period = '1y'):
    symbol = yf.Ticker(ticker)
    data = symbol.history(period)
    return data

# Function to check each stock
def check_stock(symbol):
    try:
        # Fetch stock data
        stock = yf.Ticker(symbol)
        data = stock.history(period="1y") 
        # other_data = yf.download(symbol, period="1mo")
        # Check if data was retrieved correctly
        if data.empty:
            print(f"No historical data found for {symbol} | Not older than a year")
            return f"No historical data found for {symbol} | Not older than a year"
        # Calculate RSI
        data['RSI'] = ta.momentum.RSIIndicator(data['Close']).rsi()
        # Get the latest available data

        latest_data = stock.info
        # Check if forward P/E ratio and EPS data are available
        pe_ratio = latest_data.get('forwardPE', None)
        current_ratio = latest_data.get('currentRatio', None)
        quick_ratio = latest_data.get('quickRatio', None)
        roe = latest_data.get('returnOnEquity', None)
        gross_margin = latest_data.get('grossMargins', None)
        if pe_ratio is None or current_ratio is None or quick_ratio is None:
            print(f"Missing essential financial data for {symbol}")
            return f"Missing essential financial data for {symbol}"
       
        # Get the latest RSI value
        latest_rsi = data['RSI'].iloc[-1] if not data['RSI'].empty else None
        
        # Check if the RSI data is available
        if latest_rsi is None:
            print(f"RSI data is missing or incomplete for {symbol}")
            return f"RSI data is missing or incomplete for {symbol}"
        
        bool_pe_ratio = pe_ratio < thresholds.get("pe_ratio_threshold")
        bool_current_ratio = current_ratio > thresholds.get("current_ratio_threshold")
        bool_quick_ratio = quick_ratio > thresholds.get("quick_ratio_threshold")
        bool_roe = roe > thresholds.get("roe_threshold")
        bool_gross_margin = gross_margin > thresholds.get("gross_margin_threshold")
        # Evaluate the financial health
        
        if (bool_pe_ratio and
            bool_current_ratio and
            bool_quick_ratio and
            bool_roe and
            bool_gross_margin):

            buying_opportunities.append({
                'Symbol': symbol,
                'PE Ratio': pe_ratio,
                'RSI': latest_rsi,
                'Current Ratio': current_ratio,
                'Quick Ratio': quick_ratio,
                'ROE': roe,
                'Gross Margin': gross_margin,
            })

        financial_data = (
            f"Symbol {symbol:>20}\n"
            f"PE Ratio: {round(pe_ratio, 2):>18} {'✅' if bool_pe_ratio else '❌':>5}\n"
            f"Current Ratio: {round(current_ratio, 2):>10} {'✅' if bool_current_ratio else '❌':>5}\n"
            f"Quick Ratio: {round(quick_ratio, 2):>12} {'✅' if bool_quick_ratio else '❌':>5}\n"
            f"ROE: {round(roe, 2):>26} {'✅' if bool_roe else '❌':>5}\n"
            f"Gross Margin: {round(gross_margin, 2):>9} {'✅' if bool_gross_margin else '❌':>5}\n"
            f"\nIndicators\n"
            f"RSI: {round(latest_rsi, 2):>28}"
        )
    
        return financial_data
            
    except Exception as e:
        print(f"Error checking {symbol}: {e}")
        return(f"Error checking {symbol}: {e}")

def get_symbols(scan_location = 'america'):
    try:
        url = f'https://scanner.tradingview.com/{scan_location}/scan'
        data = requests.get(url)
        if data.status_code == 200:
            json_result = json.loads(data.content)
            values = [item["s"].split(":")[1] for item in json_result["data"]]
    except Exception as e:
        print(f"Error getting symbols: {e}")
        return(f"Error getting symbols: {e}")