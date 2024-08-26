import requests

def fetch_symbols(scan_location='america'):

    if scan_location.lower() == 'debug':
        symbols =( 'DEBUG:GME', 'DEBUG:MOFG', 'DEBUG:HOFV', 'DEBUG:JCSE', 'DEBUG:STRR', 'DEBUG:UONE', 'DEBUG:DJCO', 'DEBUG:MCAGU', 'DEBUG:DSY', 'DEBUG:SLDP',
        'DEBUG:OXSQ', 'DEBUG:RRR', 'DEBUG:VRA', 'DEBUG:YHGJ', 'DEBUG:COLL', 'DEBUG:FSHPU', 'DEBUG:JTEK', 'DEBUG:FIVN', 'DEBUG:TBRG', 'DEBUG:RPD', 'DEBUG:BTCT',
        'DEBUG:BHRB', 'DEBUG:LBTYK', 'DEBUG:RFAIU', 'DEBUG:RFAC', 'DEBUG:CEAD', 'DEBUG:POOL', 'DEBUG:SRBK', 'DEBUG:ON', 'DEBUG:KELYB', 'DEBUG:MTSI', 'DEBUG:FCA',
        'DEBUG:ESEA', 'DEBUG:STSS', 'DEBUG:XP', 'DEBUG:NVMI', 'DEBUG:SOGP', 'DEBUG:FRST', 'DEBUG:ARCC', 'DEBUG:MVST', 'DEBUG:RKLB', 'DEBUG:TMC', 'DEBUG:BBSI',
        'DEBUG:GLSI', 'DEBUG:INOD', 'DEBUG:AMLI', 'DEBUG:NMTC', 'DEBUG:RNAC', 'DEBUG:NUTX', 'DEBUG:ULH', 'DEBUG:NTNX', 'DEBUG:ULCC', 'DEBUG:CSF', 'DEBUG:SMCI',
        'DEBUG:PSCD', 'DEBUG:SHPH', 'DEBUG:PLMI', 'DEBUG:INBX', 'DEBUG:IBIT', 'DEBUG:BANX', 'DEBUG:CAMT', 'DEBUG:HUBC', 'DEBUG:PSCF', 'DEBUG:BGXX', 'DEBUG:IART',
        'DEBUG:TXG', 'DEBUG:AGNCP', 'DEBUG:MNTL', 'DEBUG:PRLD', 'DEBUG:ALLR', 'DEBUG:CDTG', 'DEBUG:PDBC', 'DEBUG:PLAB', 'DEBUG:KZR', 'DEBUG:SAFT', 'DEBUG:SOWG',
        'DEBUG:SLS', 'DEBUG:AFBI', 'DEBUG:MGRM', 'DEBUG:CCNE', 'DEBUG:CRBU', 'DEBUG:PCSA', 'DEBUG:ROP', 'DEBUG:LFVN', 'DEBUG:COLM', 'DEBUG:AEYE', 'DEBUG:PFM', 'DEBUG:UNB')
        return clean_symbols(symbols)

    try:
        url = f'https://scanner.tradingview.com/{scan_location.lower()}/scan'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        symbols = [item["s"] for item in data.get("data", [])]
        return clean_symbols(symbols)

    except requests.RequestException as e:
        print(f"Error fetching symbols: {e}")
        return []

def clean_symbols(symbols):

    return [{"exchange": i.split(":")[0], "ticker": i.split(":")[1]} for i in symbols if '/' not in i and '.' not in i]

def get_symbols(scan_location='america', symbols=None):
    if not symbols:
        symbols = fetch_symbols(scan_location)
    return [s["ticker"] for s in symbols]

def get_symbols_by_exchange(scan_location='america', exchange='NASDAQ', symbols=None):
    if not symbols:
        symbols = fetch_symbols(scan_location)
    return [s["ticker"] for s in symbols if s["exchange"] == exchange.upper()]

def get_count_of_filtered_symbols(scan_location, exchange):
    return len([s for s in get_symbols_by_exchange(scan_location, exchange)])