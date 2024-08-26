import ta.momentum
import pandas as pd
import ta
from copy import deepcopy

from ticker import Ticker
from const import _EVALUATION_THRESHOLDS_, _REQUIRED_DATA
class Evaluator:

    def __init__(self):

        self.thresholds = deepcopy(_EVALUATION_THRESHOLDS_)
        self.buying_opportunities = []

    def set_threshold(self, key, value):
        self.thresholds[key] = value 

    def set_default_threshold(self):
        self.thresholds = deepcopy(_EVALUATION_THRESHOLDS_)

    def get_threshold(self, key):
        return self.thresholds.get(key)
    
    def evaluate(self, ticker):
        try:
            ticker = Ticker(ticker)

            is_ticker_valid = self.is_valid(ticker)
            if is_ticker_valid is not True:
                return None

            rsi = self.calculate_rsi(ticker.history)

            # Evaluate data against thresholds
            evaluation = {}
            evaluation['forwardPE'] = ticker.forward_pe < self.thresholds['forward_pe_threshold']
            evaluation['currentRatio'] = ticker.current_ratio > self.thresholds['current_ratio_threshold']
            evaluation['quickRatio'] = ticker.quick_ratio > self.thresholds['quick_ratio_threshold']
            evaluation['returnOnEquity'] = ticker.roe > self.thresholds['roe_threshold']
            evaluation['grossMargins'] = ticker.gross_margin > self.thresholds['gross_margin_threshold']
            
            if (evaluation['forwardPE'] and
                evaluation['currentRatio'] and
                evaluation['quickRatio'] and
                evaluation['returnOnEquity'] and
                evaluation['grossMargins']):

                data = ({
                    'Symbol': ticker.base.ticker,
                    'PE Ratio': ticker.forward_pe,
                    'Current Ratio': ticker.current_ratio,
                    'Quick Ratio': ticker.quick_ratio,
                    'ROE': ticker.roe,
                    'Gross Margin': ticker.gross_margin,
                    'RSI': rsi,
                    'Market Cap': ticker.market_cap
                })
                self.buying_opportunities.append(data)
            return None
        
        except Exception as e:
            print(f"Error checking {ticker.short_name}: {e}")
            return f"Error checking {ticker.short_name}: {e}"
        
    def generate_report(self, ticker):

        ticker = Ticker(ticker)
        is_ticker_valid = self.is_valid(ticker)
        if is_ticker_valid is not True:
            return "This ticker does not include required"
        
        # Evaluate data against thresholds
        bool_pe_ratio = ticker.forward_pe < self.thresholds['forward_pe_threshold']
        bool_current_ratio = ticker.current_ratio > self.thresholds['current_ratio_threshold']
        bool_quick_ratio = ticker.quick_ratio > self.thresholds['quick_ratio_threshold']
        bool_roe = ticker.roe > self.thresholds['roe_threshold']
        bool_gross_margin = ticker.gross_margin > self.thresholds['gross_margin_threshold']
        
        rsi = self.calculate_rsi(ticker.history)

        report = (
            f"Symbol {ticker.base.ticker:>20}\n"
            f"PE Ratio: {round(ticker.forward_pe, 2):>18} {'✅' if bool_pe_ratio else '❌':>5}\n"
            f"Current Ratio: {round(ticker.current_ratio, 2):>10} {'✅' if bool_current_ratio else '❌':>5}\n"
            f"Quick Ratio: {round(ticker.quick_ratio, 2):>12} {'✅' if bool_quick_ratio else '❌':>5}\n"
            f"ROE: {round(ticker.roe, 2):>26} {'✅' if bool_roe else '❌':>5}\n"
            f"Gross Margin: {round(ticker.gross_margin, 2):>9} {'✅' if bool_gross_margin else '❌':>5}\n"
            f"\nIndicators\n"
            f"RSI: {round(rsi, 2):>28}\n"
        )
        return report
    
    def is_valid(self, ticker: Ticker):
        try:

            if ticker.history.empty:
                raise ValueError("symbol is missing history")
            if not ticker.info:
                raise ValueError("symbol is missing information")
            
            missing_data = _REQUIRED_DATA - ticker.info.keys()

            if missing_data:
                return None
        
        except (ValueError, TypeError):
            return False
        
        return True


    def calculate_rsi(self, data):
        data['RSI'] = ta.momentum.RSIIndicator(data['Close']).rsi()
        latest_rsi = data['RSI'].iloc[-1] if not data['RSI'].empty else None
        return latest_rsi
    
    def save_opportunities_to_csv(self, file_path='buying_opportunities.csv'):
        opportunities_df = pd.DataFrame(self.buying_opportunities)
        opportunities_df.to_csv(file_path, index=False)

