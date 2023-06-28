from data import *
import re



# set_symb = reverse_search('BTCssUSD')
# print(set_symb)


def make_lib_text( name, location):
    paca_info = dict()#TradingClient('PKJRP5UHGXRG6SG4WTJ0', 'dWmrxvtgfDy9n2BwY6YAl0TFgHqszopmcdgOhgVM', paper=True).get_asset(name))
    paca_info['exchange'] = re.findall(r"\b(\w+)\b", paca_info['exchange'])[0]
    paca_info['status'] = re.findall(r"\b(\w+)\b", paca_info['status'])[0]
    paca_info['asset_class'] = re.findall(r"\b(\w+)\b", paca_info['asset_class'])[0]
    paca_info['id'] = re.sub(r'UUID\((.*?)\)', r'\1',f"{paca_info['id']}")
    exchange = paca_info['exchange']

    yf_info = yf.Ticker(name).info

    exclude= ['targetHighPrice','targetLowPrice','targetMeanPrice','targetMedianPrice','regularMarketPreviousClose','regularMarketOpen','regularMarketDayLow','regularMarketDayHigh','bid','ask''bidSize','askSize','previousClose','open','dayLow','dayHigh','companyOfficers','currentPrice','ask','bidSize']
    for ex in exclude:
        try:del yf_info[ex]
        except:pass

    match paca_info['asset_class']:
        case 'us_equity':
            alias = name
            data = {'this': f'{name}',
                    'market': f'{name}',
                    'Backtest Identifier': f'{name}',
                    'ALPACA': f'{name}',
                    'ALPACA-POSITION': f'{name}',
                    'TV_news': f'{exchange}-{name}',
                    "TV_indicators": {"symbol": f'{name}', "screener": f"{location}", "exchange": f"{exchange}"},
                    "Google_search": []}
            out = f"{alias} = \t" + f"{data | paca_info | yf_info}"
            print(re.sub(r", '", ",\n\t\t'", out))
        case _:
            print('egg')
#make_lib_text( 'LTC_USD', 'america')
def make_fx_text(this):
    nativ = {   'this':this,
                'first':this[:3],
                'second':this[4:],
                'slash':re.sub(r'_', '/', this),
                'link' : re.sub(r'_', '%2F', this),
                'yf' : re.sub(r'_', '', this) + '=X',
                'epic': f"CS.D.{re.sub(r'_', '', this)}.MINI.IP",
                "TV_indicators":{'screener':'forex'	,'exchange':'FX_IDC','symbol':re.sub(r'_', '', this)},
                'dash':re.sub(r'_', '-', this.lower())
}

    out = f"{this} = \t" + f"{nativ}"
    print(re.sub(r", '", ",\n\t\t'", out))


update_list = ['EUR_USD','EUR_CHF','NZD_USD','AUD_JPY','EUR_GBP','EUR_JPY','USD_CHF','GBP_JPY','USD_CAD','GBP_USD','AUD_USD','USD_JPY']
for li in update_list:
    make_fx_text(li)





exit()
def make_lib_crypto_text( name, location):
    paca_info = dict(TradingClient('PKJRP5UHGXRG6SG4WTJ0', 'dWmrxvtgfDy9n2BwY6YAl0TFgHqszopmcdgOhgVM', paper=True).get(name))
    paca_info['exchange'] = re.findall(r"\b(\w+)\b", paca_info['exchange'])[0]
    paca_info['status'] = re.findall(r"\b(\w+)\b", paca_info['status'])[0]
    paca_info['asset_class'] = re.findall(r"\b(\w+)\b", paca_info['asset_class'])[0]
    paca_info['id'] = re.sub(r'UUID\((.*?)\)', r'\1',f"{paca_info['id']}")
    exchange = paca_info['exchange']

    yf_info = yf.Ticker(name).info

    exclude= ['targetHighPrice','targetLowPrice','targetMeanPrice','targetMedianPrice','regularMarketPreviousClose','regularMarketOpen','regularMarketDayLow','regularMarketDayHigh','bid','ask''bidSize','askSize','previousClose','open','dayLow','dayHigh','companyOfficers','currentPrice','ask','bidSize']
    for ex in exclude:
        try:del yf_info[ex]
        except:pass

    match paca_info['asset_class']:
        case 'us_equity':
            alias = name
            data = {'this': f'{name}',
                    'market': f'{name}',
                    'Backtest Identifier': f'{name}',
                    'ALPACA': f'{name}',
                    'ALPACA-POSITION': f'{name}',
                    'TV_news': f'{exchange}-{name}',
                    "TV_indicators": {"symbol": f'{name}', "screener": f"{location}", "exchange": f"{exchange}"},
                    "Google_search": []}
            out = f"{alias} = \t" + f"{data | paca_info | yf_info}"
            print(re.sub(r", '", ",\n\t\t'", out))
        case _:
            print('egg')

make_lib_crypto_text( 'LTC_USD', 'america')


def make_lib_dict(name, location):
    paca_info = dict(TradingClient('PKJRP5UHGXRG6SG4WTJ0', 'dWmrxvtgfDy9n2BwY6YAl0TFgHqszopmcdgOhgVM', paper=True).get_asset(name))
    paca_info['exchange'] = re.findall(r"\b(\w+)\b", paca_info['exchange'])[0]
    paca_info['status'] = re.findall(r"\b(\w+)\b", paca_info['status'])[0]
    paca_info['asset_class'] = re.findall(r"\b(\w+)\b", paca_info['asset_class'])[0]
    paca_info['id'] = re.sub(r'UUID\((.*?)\)', r'\1',f"{paca_info['id']}")
    exchange = paca_info['exchange']

    yf_info = yf.Ticker(name).info

    match paca_info['asset_class']:
        case 'us_equity':
            alias = name
            data = {'this': f'{name}',
                    'market': f'{name}',
                    'Backtest Identifier': f'{name}',
                    'ALPACA': f'{name}',
                    'ALPACA-POSITION': f'{name}',
                    'TV_news': f'{exchange}-{name}',
                    "TV_indicators": {"symbol": f'{name}', "screener": f"{location}", "exchange": f"{exchange}"},
                    "Google_search": []}
            diction = data | paca_info | yf_info



        case _:
            raise Exception('THIS KEY DONT EXIST BUCKO')

    return diction







# {"AAPL": {"1W": {}, "1d": {}, "1h": {}}, "TSLA": {"1W": {}, "1d": {}, "1h": {}}, "PFE": {"1W": {}, "1d": {}, "1h": {}}, "IBM": {"1W": {}, "1d": {}, "1h": {}}}

#AAVE, BAT, BCH, BTC, DAI, ETH, GRT, LINK, LTC, MATIC, MKR, NEAR, PAXG, SHIB, SOL, UNI, USDT.