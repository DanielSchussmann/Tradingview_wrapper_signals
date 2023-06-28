import requests
from symb_LIB.symbol_lib import *

class IG_BRKR():
    def __init__(self):
        self.url = ''
        self.payload = {}
        self._cst= 'b27b88d86bcc5e4a4e19acc4f0aae34ad5522f213e954fcf2dbb3a414448b8CC01111'
        self._X_SEC ='cb058987c73fc712b8778e7d91b4ec7e9c57a50e09dcd3c48ea35f6e710929CD01111'
        self.headers ={}


    def REQ(self,protocol):
        match protocol:
            case 'GET':
                response = requests.get(self.url, headers=self.headers, json=self.payload)
                data = response.json()
                return {'data':data, 'status':response.status_code}

            case 'POST':
                response = requests.post(self.url, headers=self.headers, json=self.payload)
                data = response.json()
                return {'data':data, 'status':response.status_code}


    def GET_OPEN_POSITIONS(self):
        self.headers = {"Content-Type": "application/json; charset=UTF-8",
                        "Accept": "application/json; charset=UTF-8",
                        'X-IG-API-KEY': '34ce856dd69e8c834145ded49090fab969f1d72d',
                        'Version': '2',
                        'X-SECURITY-TOKEN': self._X_SEC,
                        'CST': self._cst}
        self.url = 'https://demo-api.ig.com/gateway/deal/positions'
        return self.REQ('GET')['data']['positions']


    def CHECK_IF_POSITION(self,symbol,short=True):

            POS = self.GET_OPEN_POSITIONS()
            for pos in POS:
                if pos['market']['epic'] == symbol['epic']:
                    out = {'dealID':pos['position']['dealId'],'size': pos['position']['size'], 'direction': pos['position']['direction'],} if short == True else pos

                    return out
            return False


    def BUY(self,symbol,qty,side,tif="EXECUTE_AND_ELIMINATE"):
        self.url = "https://demo-api.ig.com/gateway/deal/positions/otc"
        self.headers = {"Content-Type": "application/json; charset=UTF-8",
                        "Accept": "application/json; charset=UTF-8",
                        'X-IG-API-KEY': '34ce856dd69e8c834145ded49090fab969f1d72d',
                        'Version': '2',
                        'X-SECURITY-TOKEN': self._X_SEC,
                        'CST': self._cst}
        self.payload = {
            "epic": symbol["epic"],
            "expiry": "-",
            "direction": side,
            "size": str(qty),
            "orderType": "MARKET",
            "timeInForce": tif,
            "level": None,
            "guaranteedStop": "false",
            "stopLevel": None,
            "stopDistance": None,
            "trailingStop": None,
            "trailingStopIncrement": None,
            "forceOpen": "true",
            "limitLevel": None,
            "limitDistance": None,
            "quoteId": None,
            "currencyCode": symbol['second']}

        resp =self.REQ('POST')

        return resp['data']


    def SELL(self,symbol):
        data_holder = self.CHECK_IF_POSITION(symbol)
        self.url = 'https://demo-api.ig.com/gateway/deal/positions/otc'

        self.headers = {"Content-Type": "application/json; charset=UTF-8",
                        "Accept": "application/json; charset=UTF-8",
                        'X-IG-API-KEY': '34ce856dd69e8c834145ded49090fab969f1d72d',
                        'Version': '1',
                        'X-SECURITY-TOKEN': self._X_SEC,
                        'CST': self._cst,
                        '_method': 'DELETE'}

        self.payload={
            "dealId": data_holder['dealID'],
            "epic": None,
            "expiry": None,
            "direction": 'SELL' if data_holder['direction']=='BUY' else 'BUY',
            "size": '1',
            "level": None,
            "orderType": "MARKET",
            "timeInForce": "FILL_OR_KILL",
            "quoteId": None}

        out = self.REQ('POST')
        return out



ig = IG_BRKR()
check = ig.CHECK_IF_POSITION(AUD_USD)
#buy = ig.BUY(AUD_USD,1,'BUY')
#sell =ig.SELL(AUD_USD)
print(check)


