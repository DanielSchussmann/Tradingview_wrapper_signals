import oandapyV20
import oandapyV20.endpoints as OE
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.orders as orders
import oandapyV20.endpoints.trades as trades
import oandapyV20.endpoints.positions as positions

class OANDA_BROKER():
    def __init__(self):
        self._accountID = "101-004-14984531-001"
        self._client = oandapyV20.API(access_token="b3eeb82a8bb410acd8c467642069c774-082afe6b1c44a2d802b7f6131dfc78ae")

    def BUY(self ,symbol ,units):
        data = {
            "order": {
                "timeInForce": "FOK",
                "instrument": symbol  ,  # "EUR_USD",
                "units": units,  # "-100",
                "type": "MARKET",
                "positionFill": "DEFAULT"
            }
        }
        ordrs = orders.OrderCreate(self._accountID, data=data)

        # api.request(pricing.PricingInfo(accountID=self._accountID, params=params)).response

        self._client.request(ordrs)
        return ordrs.response

    def ACTIVES(self ,symbol ,simple=True):
        params = {"instrument": symbol}
        trds = trades.TradesList(accountID=self._accountID, params=params)
        self._client.request(trds)

        ordrs = orders.OrderList(self._accountID, params)
        self._client.request(ordrs)
        ordrs = ordrs.response

        pstns = positions.PositionList(accountID=self._accountID)
        self._client.request(pstns)
        pstns = pstns.response



        if simple == False:
            return pstns ,ordrs
        else:
            return pstns



    def SELL(self ,symbol):
        instrument ={"instruments": "EUR_USD"}
        data = {"longUnits": "ALL"}

        print(symbol)
        pstn = positions.PositionClose(accountID=self._accountID, instrument=instrument, data=data)

        self._client.request(pstn)
        return pstn.response

    def HANDBREAK(self):
        print('SELL EVERYTHING')




"""nda = OANDA_BROKER()

#nda.SELL('EUR_USD')
#time.sleep(10)

act = nda.ACTIVES('EUR_USD',True)

print(act)

for actvs in act['positions']:
    print( nda.SELL(actvs['instrument']))"""

"""

curl \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <AUTHENTICATION TOKEN>" \





token = 'facb549dfa82cf1cbc988644f117db56-8a203b258c582dfc5e94d35bafedd6d3'
tolken='ae5a440b17d38dceb204ea225315b015-dd0ca580e34215920c5ecebe6c73b382'
accountID='101-004-14984531-001'

head={ "Authorization": f"Bearer {tolken}"}
r = requests.get('https://api-fxtrade.oanda.com/v3/accounts',headers=head)


url = f"https://api-fxtrade.oanda.com/v3/accounts/{accountID}/positions/EUR_USD"
#url = "https://api-fxtrade.oanda.com/v3/accounts/101-004-14984531-001/changes?sinceTransactionID=6358"
#url='https://stream-fxtrade.oanda.com/v3/accounts/101-004-14984531-001/pricing/stream?instruments=EUR_USD%2CUSD_CAD'


headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}" }
#headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
#r = requests.post(url, headers=headers)


print(r.json())

class OANDA_POSTREQ():
    def __init__(self):
        self.egg='egg'










"""




