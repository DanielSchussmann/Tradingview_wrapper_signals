from tradingview_ta import *
from data import *
import openai
import numpy as np
from textblob import TextBlob
from Selenium_class import DRIVER
from selenium.webdriver.common.by import By
from GatherSignalData import *

#<-----------------------------------------------TRADINGVIEW-INDICATORS----------------------------------------------->
def TV_indicators(instrument, interval='1d',short = True):
    #'1d' '1W' '4h'
    response = TA_Handler(
    symbol=instrument['TV_indicators']['symbol'],
    screener=instrument['TV_indicators']['screener'],
    exchange=instrument['TV_indicators']['exchange'],
    interval=interval)
    resp = response.get_analysis()
    sum = resp.summary['RECOMMENDATION']
    match sum :
        case 'STRONG_BUY':
            parsed_indication = 1
        case 'BUY':
            parsed_indication = 0.75
        case 'STRONG_SELL':
            parsed_indication = 0
        case 'SELL':
            parsed_indication = 0.25
        case 'NEUTRAL':
            parsed_indication = 0.5
        case _:
            raise Exception('TV returned "  {}   " idk whta that means'.format(sum))

    return parsed_indication if short == True else resp.summary


#print(TV_indicators(EUR_USD))




def DFX_sentiment(symbol,short=True,l_1=1,l_2=1,l_3=1):
    sentiment = get_DFX_sentiment(symbol).to_dict(orient='records')[0]
    match sentiment['Signal']:
        case 'BEARISH':
            simple_sentiment = 0
            #complex_sentiment = 0
        case 'BULLISH':
            simple_sentiment = 1
            #complex_sentiment = 1
        case 'MIXED':
            simple_sentiment = 0.5
            #complex_sentiment = 0.5
    #low OI \ high NET \ low Change in both means trend will continue -> DONT CHANGE OPEN POSIITON, neutral on new entry
    complex_long = l_1 * sentiment['Net long'] + l_2 * sentiment['Change_long'] + (l_3 * sentiment['Change oi'] if sentiment['Change oi'] >= 0 else 0)
    complex_short =l_1 * sentiment['Net short'] + l_2 * sentiment['Change_short'] + (l_3 * sentiment['Change oi'] if sentiment['Change oi'] <= 0 else 0)


    out_short = {'simple_sentiment':simple_sentiment,'complex_sentiment':complex_long}
    out_long = sentiment

    return out_short if short == True else sentiment



print(DFX_sentiment(AUD_JPY,False))







def news_GPT(symbol,numeral = True):
    out = []
    for x in news(symbol): out.append(x['title'])
    openai.api_key = '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'
    messages = [{"role": "user", "content": 'analyse {}, return python list with BULLISH, BEARISH or NEUTRAL for each headline'.format(out)} ]
    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    ret = chat.choices[0].message.content

    num_ret = 1
    for indi in ret:
        match indi:
            case 'BULLISH':
                num_ret += 0.1
            case 'BEARISH':
                num_ret -= 0.1
            case 'NEUTRAL':
                num_ret
            case _:
                raise Exception(indi + 'is not a set parameter')


    return ret if numeral == False else num_ret

def news_BLOB(symbol):
    def get_sentiment_score(headline):
        blob = TextBlob(headline)
        sentiment = blob.sentiment.polarity
        if sentiment > 0:
            return 1.0  # BULLISH
        elif sentiment < 0:
            return 0.0  # BEARISH
        else:
            return 0.5  # NEUTRAL

    headlines = [s['title'] for s in news(symbol)]

    sentiment_scores = [get_sentiment_score(h) for h in headlines]
    return np.average(sentiment_scores)
#print(news_BLOB(TSLA))




def TV_news(symbol,limit=20,complex=False):
    x = DRIVER()
    x.set_standard_options()
    x.start()
    driver = x.driver
    driver.get(f'https://www.tradingview.com/symbols/{symbol["TV_news"]}/news/')

    def get_sentiment_score(headline):
        blob = TextBlob(headline)
        sentiment = blob.sentiment.polarity
        if sentiment > 0:
            return 1.0  # BULLISH
        elif sentiment < 0:
            return 0.0  # BEARISH
        else:
            return 0.5  # NEUTRAL

    #GET THE DATA
    ret ={'sentiment_scores':[] ,'titles':[],'FULL':[]}
    for i in driver.find_elements(By.CSS_SELECTOR,'.card-exterior-Us1ZHpvJ.article-rY32JioV')[0:limit]:
        try:
            time= i.find_element(By.TAG_NAME,'relative-time').get_attribute('event-time')
        except:
            time = i.find_element(By.TAG_NAME, 'time').get_attribute('datetime')

        title = i.find_elements(By.TAG_NAME, 'span')[-1].text
        s_score = get_sentiment_score(title)

        ret['titles'].append(title)
        ret['FULL'].append({'time':time,'title':title , 's_score':s_score})
        ret['sentiment_scores'].append(s_score)


    ret['sentiment_score'] = np.average(ret['sentiment_scores'])
    x.stop()
    return ret if complex == True else ret['sentiment_score']




#print(TV_news(IBM,20))


