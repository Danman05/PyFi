import yfinance as yf
import ta
import requests
import json


# Define parameters for your strategy
pe_ratio_threshold = 20  # Stocks with a P/E ratio below this are considered undervalued
rsi_threshold = 30        # RSI below 30 indicates oversold conditions
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
            print(f"No historical data found for {symbol}")
            return f"No historical data found for {symbol}"
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
        
        # Evaluate the financial health
        if (pe_ratio < pe_ratio_threshold and
            current_ratio is not None and current_ratio > 1 and
            quick_ratio is not None and quick_ratio > 1 and
            roe is not None and roe > 0 and
            gross_margin is not None and gross_margin > 0):

            buying_opportunities.append({
                'Symbol': symbol,
                'PE Ratio': pe_ratio,
                'RSI': latest_rsi,
                'Current Ratio': current_ratio,
                'Quick Ratio': quick_ratio,
                'ROE': roe,
                'Gross Margin': gross_margin,
            })
            result = f"Symbol: {symbol}\nPE Ratio: {pe_ratio}\nRSI: {latest_rsi}\nCurrent Ratio: {current_ratio}\nQuick Ratio: {quick_ratio}\nROE: {roe}\nGross Margin: {gross_margin}"
            return result
            
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