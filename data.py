import yfinance as yf
from time import strftime, localtime


def cpr(symbol,period='1d',interval='1d'): #current price
    data = yf.Ticker(symbol['market']).history(period=period)#,interval=interval)

    return float(data['Close'])

def pr(symbol):#PRICE RANGE
    data = yf.Ticker(symbol['market']).history()  # ,interval=interval)

def news(symbol):
    data = yf.Ticker(symbol['market'])
    ret = []
    for story in data.news:
        tme = strftime('%Y-%m-%d %H:%M:%S', localtime(story['providerPublishTime']))
        ret.append({'title':story['title'],'time':tme, 'uuid':story['uuid'], 'publisher':story['publisher'] })
    return ret



#print(yf.Ticker('EURUSD=X').info)
#for x in news(PFE):print(x['title'],x['time'])
#print(cpr(EUR_USD,'1h'))