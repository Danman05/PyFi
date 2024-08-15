import ta

class FinancialData:
    def __init__(self, data: dict):
        self.pe_ratio = data.get('forwardPE')
        self.current_ratio = data.get('currentRatio')
        self.quick_ratio = data.get('quickRatio')
        self.roe = data.get('returnOnEquity')
        self.gross_margin = data.get('grossMargins')
        self.market_cap = data.get('marketCap')
    
    def is_valid(self):
        required_metrics = [self.pe_ratio, self.current_ratio, self.quick_ratio, self.roe, self.gross_margin]
        missing_metrics = [metric for metric in required_metrics if metric is None]
        
        if missing_metrics:
            return False, f"Missing essential financial data: {', '.join(missing_metrics)}"
        
        try:
            self.pe_ratio = float(self.pe_ratio)
            self.current_ratio = float(self.current_ratio)
            self.quick_ratio = float(self.quick_ratio)
            self.roe = float(self.roe)
            self.gross_margin = float(self.gross_margin)
        except (ValueError, TypeError) as e:
            return False, f"Error processing financial data: {e}"
        
        return True, None
    
    def get_metrics(self):
        return {
            'PE Ratio': self.pe_ratio,
            'Current Ratio': self.current_ratio,
            'Quick Ratio': self.quick_ratio,
            'ROE': self.roe,
            'Gross Margin': self.gross_margin
        }

class StockEvaluator:
    def __init__(self, symbol, data, financial_data, thresholds):
        self.symbol = symbol
        self.data = data
        self.financial_data = financial_data
        self.thresholds = thresholds
    
    def calculate_rsi(self):
        self.data['RSI'] = ta.momentum.RSIIndicator(self.data['Close']).rsi()
        self.latest_rsi = self.data['RSI'].iloc[-1] if not self.data['RSI'].empty else None

        if self.latest_rsi is None:
            return False, f"{self.symbol}: RSI data is missing or incomplete."
        return True, None
    
    def evaluate(self):
        valid, error = self.financial_data.is_valid()
        if not valid:
            return None, error
        
        rsi_valid, rsi_error = self.calculate_rsi()
        if not rsi_valid:
            return None, rsi_error
        
        metrics = self.financial_data.get_metrics()
        if (metrics['PE Ratio'] < self.thresholds["pe_ratio_threshold"] and
            metrics['Current Ratio'] > self.thresholds["current_ratio_threshold"] and
            metrics['Quick Ratio'] > self.thresholds["quick_ratio_threshold"] and
            metrics['ROE'] > self.thresholds["roe_threshold"] and
            metrics['Gross Margin'] > self.thresholds["gross_margin_threshold"]):
            
            return {
                'Symbol': self.symbol,
                'Metrics': metrics,
                'RSI': self.latest_rsi,
                'Market Cap': self.financial_data.market_cap
            }, None
        return None, None

    def generate_report(self, evaluation_result):
        if not evaluation_result:
            return f"No buying opportunity for {self.symbol}"
        
        financials = evaluation_result['Metrics']
        bool_pe_ratio = financials['PE Ratio'] < self.thresholds["pe_ratio_threshold"]
        bool_current_ratio = financials['Current Ratio'] > self.thresholds["current_ratio_threshold"]
        bool_quick_ratio = financials['Quick Ratio'] > self.thresholds["quick_ratio_threshold"]
        bool_roe = financials['ROE'] > self.thresholds["roe_threshold"]
        bool_gross_margin = financials['Gross Margin'] > self.thresholds["gross_margin_threshold"]

        report = (
            f"Symbol {self.symbol:>20}\n"
            f"PE Ratio: {round(financials['PE Ratio'], 2):>18} {'✅' if bool_pe_ratio else '❌':>5}\n"
            f"Current Ratio: {round(financials['Current Ratio'], 2):>10} {'✅' if bool_current_ratio else '❌':>5}\n"
            f"Quick Ratio: {round(financials['Quick Ratio'], 2):>12} {'✅' if bool_quick_ratio else '❌':>5}\n"
            f"ROE: {round(financials['ROE'], 2):>26} {'✅' if bool_roe else '❌':>5}\n"
            f"Gross Margin: {round(financials['Gross Margin'], 2):>9} {'✅' if bool_gross_margin else '❌':>5}\n"
            f"\nIndicators\n"
            f"RSI: {round(evaluation_result['RSI'], 2):>28}\n"
        )
        return report