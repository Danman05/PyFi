class FinancialData:
    
    # Define what data you want to analyse
    def __init__(self, data: dict):
                
        pass
    
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
        