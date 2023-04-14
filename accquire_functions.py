from tradingview_ta import *


#print(Interval.INTERVAL_4_HOURS)



def TV_indicators(instrument, interval='1d',simple = True):
    #'1d' '1W' '4h'
    response = TA_Handler(
    symbol=instrument['TV_indicators']['symbol'],
    screener=instrument['TV_indicators']['screener'],
    exchange=instrument['TV_indicators']['exchange'],
    interval=interval#interval_parser(interval)
    )

    return response.get_analysis().summary['RECOMMENDATION'] if simple == True else response.get_analysis().summary



