from utils import validate_period
from yf_fetcher import fetch_ticker, fetch_ticker_info, fetch_ticker_history

class Ticker:
    def __init__(self, ticker, skip_info = False, skip_history = False, history_period = 'ytd'):
        self.base = fetch_ticker(ticker)
        self.history_period = history_period
        self.info = {}
        self.history = {}
        if not skip_info:
            self.info = fetch_ticker_info(ticker)

        if not skip_history:
            self.history = fetch_ticker_history(ticker, self.history_period)


        # region Financial Ratios
        self.forward_pe = self.info.get('forwardPE')
        self.trailing_pe = self.info.get('trailingPE')
        self.current_ratio = self.info.get('currentRatio')
        self.quick_ratio = self.info.get('quickRatio')
        self.roe = self.info.get('returnOnEquity')
        if self.roe is not None:
            self.roe*=100
        self.gross_margin = self.info.get('grossMargins')
        self.market_cap = self.info.get('marketCap')
        self.enterprise_value = self.info.get('enterpriseValue')
        self.profit_margins = self.info.get('profitMargins')
        self.price_to_book = self.info.get('priceToBook')
        self.price_to_sales = self.info.get('priceToSalesTrailing12Months')
        self.debt_to_equity = self.info.get('debtToEquity')
        self.ebitda = self.info.get('ebitda')
        self.total_debt = self.info.get('totalDebt')
        self.total_cash = self.info.get('totalCash')
        self.free_cashflow = self.info.get('freeCashflow')
        # endregion

        # region Basic Information
        self.address = self.info.get('address1')
        self.city = self.info.get('city')
        self.state = self.info.get('state')
        self.zip_code = self.info.get('zip')
        self.country = self.info.get('country')
        self.phone = self.info.get('phone')
        self.website = self.info.get('website')
        self.industry = self.info.get('industry')
        self.sector = self.info.get('sector')
        self.long_business_summary = self.info.get('longBusinessSummary')
        self.full_time_employees = self.info.get('fullTimeEmployees')
        # endregion

        # region Market info
        self.current_price = self.info.get('currentPrice')
        self.target_high_price = self.info.get('targetHighPrice')
        self.target_low_price = self.info.get('targetLowPrice')
        self.target_mean_price = self.info.get('targetMeanPrice')
        self.target_median_price = self.info.get('targetMedianPrice')
        self.previous_close = self.info.get('previousClose')
        self.open_price = self.info.get('open')
        self.day_low = self.info.get('dayLow')
        self.day_high = self.info.get('dayHigh')
        self.fifty_two_week_low = self.info.get('fiftyTwoWeekLow')
        self.fifty_two_week_high = self.info.get('fiftyTwoWeekHigh')
        self.volume = self.info.get('volume')
        self.average_volume = self.info.get('averageVolume')
        self.average_ten_days_volume = self.info.get('averageDailyVolume10Day')
        # endregion

        # region Risk Metrics
        self.audit_risk = self.info.get('auditRisk')
        self.board_risk = self.info.get('boardRisk')
        self.compensation_risk = self.info.get('compensationRisk')
        self.shareholder_rights_risk = self.info.get('shareHolderRightsRisk')
        self.overall_risk = self.info.get('overallRisk')
        # endregion

        # region Company Officers
        self.company_officers = self.info.get('companyOfficers')
        # endregion

        # region Other
        self.currency = self.info.get('currency')
        self.exchange = self.info.get('exchange')
        self.quote_type = self.info.get('quoteType')
        self.symbol = self.info.get('symbol')
        self.short_name = self.info.get('shortName')
        self.long_name = self.info.get('longName')
        self.uuid = self.info.get('uuid')
        self.time_zone_full_name = self.info.get('timeZoneFullName')
        self.time_zone_short_name = self.info.get('timeZoneShortName')
        self.gmt_offset_milliseconds = self.info.get('gmtOffSetMilliseconds')
        self.financial_currency = self.info.get('financialCurrency')
        # endregion

    def set_history(self, raw_period):

        period = str(raw_period)
        validate_period(period)
        
        self.history = self.base.history(period)
        self.history_period = period