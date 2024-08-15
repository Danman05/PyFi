from utils import validate_period
from Fetchers.yf_fetcher import fetch_ticker, fetch_ticker_info, fetch_ticker_history

class Ticker:
    def __init__(self, ticker, skip_info = False, skip_history = False, history_period = 'ytd'):

        self.base = fetch_ticker(ticker)
        self.ticker_history_period = history_period

        if not skip_info:
            self.ticker_info = fetch_ticker_info(ticker)

        if not skip_history:
            self.ticker_history = fetch_ticker_history(ticker, self.ticker_history_period)


        # region Financial Ratios
        self.pe_ratio = self.ticker_info.get('forwardPE')
        self.current_ratio = self.ticker_info.get('currentRatio')
        self.quick_ratio = self.ticker_info.get('quickRatio')
        self.roe = self.ticker_info.get('returnOnEquity')
        self.gross_margin = self.ticker_info.get('grossMargins')
        self.market_cap = self.ticker_info.get('marketCap')
        self.enterprise_value = self.ticker_info.get('enterpriseValue')
        self.profit_margins = self.ticker_info.get('profitMargins')
        self.price_to_book = self.ticker_info.get('priceToBook')
        self.price_to_sales = self.ticker_info.get('priceToSalesTrailing12Months')
        self.debt_to_equity = self.ticker_info.get('debtToEquity')
        self.ebitda = self.ticker_info.get('ebitda')
        self.total_debt = self.ticker_info.get('totalDebt')
        self.total_cash = self.ticker_info.get('totalCash')
        self.free_cashflow = self.ticker_info.get('freeCashflow')
        # endregion

        # region Basic Information
        self.address = self.ticker_info.get('address1')
        self.city = self.ticker_info.get('city')
        self.state = self.ticker_info.get('state')
        self.zip_code = self.ticker_info.get('zip')
        self.country = self.ticker_info.get('country')
        self.phone = self.ticker_info.get('phone')
        self.website = self.ticker_info.get('website')
        self.industry = self.ticker_info.get('industry')
        self.sector = self.ticker_info.get('sector')
        self.long_business_summary = self.ticker_info.get('longBusinessSummary')
        self.full_time_employees = self.ticker_info.get('fullTimeEmployees')
        # endregion

        # region Market self.ticker_info
        self.current_price = self.ticker_info.get('currentPrice')
        self.target_high_price = self.ticker_info.get('targetHighPrice')
        self.target_low_price = self.ticker_info.get('targetLowPrice')
        self.target_mean_price = self.ticker_info.get('targetMeanPrice')
        self.target_median_price = self.ticker_info.get('targetMedianPrice')
        self.previous_close = self.ticker_info.get('previousClose')
        self.open_price = self.ticker_info.get('open')
        self.day_low = self.ticker_info.get('dayLow')
        self.day_high = self.ticker_info.get('dayHigh')
        self.fifty_two_week_low = self.ticker_info.get('fiftyTwoWeekLow')
        self.fifty_two_week_high = self.ticker_info.get('fiftyTwoWeekHigh')
        self.volume = self.ticker_info.get('volume')
        self.average_volume = self.ticker_info.get('averageVolume')
        self.average_ten_days_volume = self.ticker_info.get('averageDailyVolume10Day')
        # endregion

        # region Risk Metrics
        self.audit_risk = self.ticker_info.get('auditRisk')
        self.board_risk = self.ticker_info.get('boardRisk')
        self.compensation_risk = self.ticker_info.get('compensationRisk')
        self.shareholder_rights_risk = self.ticker_info.get('shareHolderRightsRisk')
        self.overall_risk = self.ticker_info.get('overallRisk')
        # endregion

        # region Company Officers
        self.company_officers = self.ticker_info.get('companyOfficers')
        # endregion

        # region Other
        self.currency = self.ticker_info.get('currency')
        self.exchange = self.ticker_info.get('exchange')
        self.quote_type = self.ticker_info.get('quoteType')
        self.symbol = self.ticker_info.get('symbol')
        self.short_name = self.ticker_info.get('shortName')
        self.long_name = self.ticker_info.get('longName')
        self.uuid = self.ticker_info.get('uuid')
        self.time_zone_full_name = self.ticker_info.get('timeZoneFullName')
        self.time_zone_short_name = self.ticker_info.get('timeZoneShortName')
        self.gmt_offset_milliseconds = self.ticker_info.get('gmtOffSetMilliseconds')
        self.financial_currency = self.ticker_info.get('financialCurrency')
        # endregion

    def set_history(self, raw_period):

        period = str(raw_period)
        validate_period(period)
        
        self.ticker_history = self.ticker.history(period)
        self.ticker_history_period = period


