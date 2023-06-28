from INDICATORS import *
from strat_framework import *
#START STATS
"""
TIMEFRAME 
    \_4H
INDICATORS
    \_TV-indicators
    \_TV-news

TRIGGERS
    \_long if score above 0.8, short if score below 0.2
    \_sell long if position is below 0.5, sell short if position is above 0.5
"""



strat = STRAT()
buy_rating = INDICATOR_RATING()
sell_rating = INDICATOR_RATING()
strat.symbols=[AAPL,IBM,GOOGL,PFE]
strat.broker.frac = '4h'

buy_rating.indicators = [TV_indicators,TV_news]
buy_rating.weights = [1,0.8]

sell_rating.indicators = [TV_indicators,TV_news]
sell_rating.weights = [1,0.8]
#broker.BUY(TSLA,100,'LON G','day',False) #BUY FOR 100 EUR





def buy_frame(symbol):
    buy_rating.get_rating(symbol)
    print(f":::: {symbol['this']}-{buy_rating.info_data} ::::")

    if buy_rating.weighted_rating >= 0.6 and buy_rating.weighted_spread <= 0.4:
        print(f':::: shorted $100 worth of {symbol["ALPACA"]}::::')
        return {'symbol':symbol,'qty':100,'tif':'day','side':'LONG'}

    elif buy_rating.weighted_rating <= 0.3 and buy_rating.weighted_spread <= 0.4:
        print(f':::: shorted $100 worth of {symbol["ALPACA"]}::::')
        return {'symbol':symbol,'qty':100,'tif':'day','side':'SHORT'}
    else:
        return False


def sell_frame(symbol,side):
    sell_rating.get_rating(symbol)
    print(f":::: {symbol['this']}-{sell_rating.info_data} ::::")

    match side:
        case 'LONG':
            if sell_rating.weighted_rating < 0.5 and sell_rating.weighted_spread <= 0.6:
                print(f":::: {symbol['this']}- SOLD ::::")
                return True
            else:
                return False
        case 'SHORT':
            if sell_rating.weighted_rating > 0.5 and sell_rating.weighted_spread <= 0.6:
                print(f":::: {symbol['this']}- SOLD ::::")
                return True
            else:
                return False


strat.buy_frame = buy_frame
strat.sell_frame = sell_frame

strat.loop()

"""    #<-----SELL-LOGIC---->
for sy in symbols:
        try:
            side = broker.CHECK_FULL(sy).side
        except:
            continue

        rating.get_rating(sy)
        print('ss')
        match side:
            case 'LONG':
                if rating.weighted_rating < 0.5 and rating.weighted_spread <= 0.6:
                    broker.SELL(sy) # SELL
                    time.sleep(5)

            case 'SHORT':
                if rating.weighted_rating > 0.5 and rating.weighted_spread <= 0.6:
                    broker.SELL(sy)  # SELL
                    time.sleep(5)


    print(f"#### {broker.OPEN_PL()} ####")

"""



