from concurrent.futures import ThreadPoolExecutor
import numpy as np

from evaluator import Evaluator
from symbol_fetcher import get_symbols_by_exchange

class Scanner:

    def  __init__(self):
        self.opportunities = []

    def scan_symbols(self, exchange= 'NASDAQ', scan_location='america', symbols=None, workers=10, evaluator = Evaluator()):
        print(f"scanning symbols with {workers} workers")
        if not symbols:
            symbols = get_symbols_by_exchange(scan_location=scan_location, exchange=exchange)
        
        # I would have passed in Ticker(s) to the evaluate method, but it seems to block the working threads, so Ticker object is made later
        with ThreadPoolExecutor(max_workers=workers) as executor: 
            {executor.submit(evaluator.evaluate, s): s for s in np.sort(symbols) if '/' not in s and '.' not in s}
            