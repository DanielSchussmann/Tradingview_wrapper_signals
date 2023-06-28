import oandapyV20
import oandapyV20.endpoints as OE
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.orders as orders
import time
import datetime
import openai

# client = oandapyV20.API(access_token=...)

accountID = "101-004-14984531-001"
client = oandapyV20.API(access_token="b3eeb82a8bb410acd8c467642069c774-082afe6b1c44a2d802b7f6131dfc78ae")


def time_parser(typ,input): #HAS TO BE DATETIME.DATETIME

    match typ:
        case 'oanda':
            ret = time.mktime(input.timetuple())
        case _:
            ret = 'N.A.N'
    return ret


#print(time_parser('oanda',datetime.datetime(2023, 4, 20, 14, 30, 0)))






def get_price_range(candle, symbol, time_from, time_to='now', granularity='D'):
    if time_to == 'now': time_to = time.time()

    params = {
        "granularity": granularity,
        "from": "1654214400",
        "to": time_to
    }
    r = instruments.InstrumentsCandles(instrument=symbol, params=params)
    # print(time.time()- 365*24*60*60)
    client.request(r)
    rep = r.response

    match candle:
        case 'open':
            ret = rep['candles'][-1]['mid']['o']
        case 'close':
            ret = rep['candles'][-1]['mid']['c']
        case 'high':
            ret = rep['candles'][-1]['mid']['h']
        case 'low':
            ret = rep['candles'][-1]['mid']['l']
        case _:
            ret = 'ERROR'

    return ret



openai.api_key = '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'
"""messages = [ {"role": "system", "content":
              "You are a intelligent assistant."} ]
while True:
    message = input("User : ")
    if message:
        messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
    reply = chat.choices[0].message.content
    print(f"ChatGPT: {reply}")
    messages.append({"role": "assistant", "content": reply})
"""
#print(get_price_range('open',"EUR_USD"))

messages = [{"role": "user", "content": 'is there a way to make python requests wait before it returns a response'}]
chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
reply = chat.choices[0].message.content
print(f"ChatGPT: {reply}")

