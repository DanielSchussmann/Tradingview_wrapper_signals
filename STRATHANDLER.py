import pandas as pd
import requests
from symb_LIB.symbol_lib import *

API_KEY = 'PKJRP5UHGXRG6SG4WTJ0'
SECRET_KEY = 'dWmrxvtgfDy9n2BwY6YAl0TFgHqszopmcdgOhgVM'

def GET_TRANSACTIONS(symbol):
    pd.set_option('display.max_columns', None)  # Set the maximum number of columns to None
    headers = {
        'APCA-API-KEY-ID': f'{API_KEY}',
        'APCA-API-SECRET-KEY': f'{SECRET_KEY}'
    }

    response = requests.get('https://paper-api.alpaca.markets/v2/account/activities' , headers=headers)
    act = response.json()


    df = pd.DataFrame(act)
    df['USD'] = pd.to_numeric(df['qty'], errors='coerce')* pd.to_numeric(df['price'], errors='coerce')
    df_req = df[['symbol','USD','side','type','price','qty','order_id','transaction_time']].sort_values(['symbol', 'transaction_time'],ascending=[True,False])
    df_isolated = df_req.loc[df['symbol'] == symbol['this']]


    return df_isolated

print(GET_TRANSACTIONS(TSLA)[['USD','side','type','order_id']])

