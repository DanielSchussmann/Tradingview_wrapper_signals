from Selenium_class import *
import pandas as pd
import os
from datetime import datetime  as dtm
import time
from symb_LIB.symbol_lib import *


sentiment_SYMBOLS=[EUR_USD,EUR_CHF,NZD_USD,AUD_JPY,EUR_GBP,EUR_JPY,USD_CHF,GBP_JPY,USD_CAD,GBP_USD,AUD_USD,USD_JPY,OIL_US,CRUDE,SILVER,GOLD,US_500,WALL_STREET,GERMANY_40,FTSE_100,FRANCE_40]



def FILE_IN_DIR(dir,key):
    files = os.listdir(dir)
    match key:
        case 'newest':
            file_name = max(files, key=lambda f: os.path.getmtime(os.path.join(dir, f)))
            out_file = {'name':file_name,'TimeStamp':dtm.fromtimestamp(os.path.getmtime(dir+file_name)),"path":dir+file_name}
        case 'oldest':
            file_name = min(files, key=lambda f: os.path.getmtime(os.path.join(dir, f)))
            out_file = {'name':file_name,'TimeStamp':dtm.fromtimestamp(os.path.getmtime(dir+file_name)),"path":dir+file_name}
        case 'all' :
            out_file = [ {'name':file_name,'TimeStamp':dtm.fromtimestamp(os.path.getmtime(dir+file_name)),"path":dir+file_name} for file_name in files]
        case _:
            raise Exception("Key(second parameter) for FILE_IN_DIR() needs to be 'newest' or 'oldest' or 'all'")

    return out_file # Returns a file name and the associated timestamp
#print(FILE_IN_DIR('SENTIMENT/sentiment_CSVs/','all'))


#print(os.path.getmtime('SENTIMENT/sentiment_CSVs/'+'2023-06-22 15:47:24.709137.csv'))

#-----Get-Data--------------------------------->
def get_DFX_sentiment(symbol = {'slash':'all'}):

    file = FILE_IN_DIR('/Users/dnsn/Documents/DEOS_al_tradier/TradingSignalScraper/SENTIMENT/sentiment_CSVs/', 'newest')
    df = pd.read_csv(file['path'])
    if symbol['slash'] == 'all': return df

    else:
        matching_rows = df[df['Symbol'].str.contains(symbol['slash'])]
        return matching_rows


#print(get_DFX_sentiment(AUD_USD))
#print(sentiment({'sentiment':'EUR/USD'}))


