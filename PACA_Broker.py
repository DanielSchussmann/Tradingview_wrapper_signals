from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide
from data import *
import json

class ALPACA_BROKER():
    """
        This class represents an Alpaca broker for trading operations.

        Attributes:
            _API_KEY (str): The API key for the Alpaca broker.
            _SECRET_KEY (str): The secret key for the Alpaca broker.
            _trading_client (TradingClient): The Alpaca trading client.
            frac (bool): The timeframe flag for fractional quantities.

        Methods:
            STATUS(): Retrieves the status of the Alpaca trading clock.
            BUY(symbol, qty, side, tif, check=True): Places a buy market order for a given symbol.
            SELL(symbol, check=True): Sells an open position for a given symbol.
            CHECK_IF_POSITION(symbol): Checks if there is an open position for a given symbol.
            CHECK_IF_ORDER(symbol): Checks if there is an open order for a given symbol.
            CHECK_FULL(symbol): Checks if the symbol is tradable and has any open orders or positions.
            OPEN_POSITIONS(): Retrieves all open positions.
            OPEN_PL(): Retrieves the total unrealized profit/loss and individual position details.
            FULL_INFO(): Retrieves the full information about available assets.
        """

    def __init__(self):
        self.name = 'default'
        self._API_KEY = 'PKJRP5UHGXRG6SG4WTJ0'
        self._SECRET_KEY = 'dWmrxvtgfDy9n2BwY6YAl0TFgHqszopmcdgOhgVM'
        self._trading_client = TradingClient(self._API_KEY, self._SECRET_KEY, paper=True)
        self.frac = False # set as the timeframe


    def STATUS(self):
            # add .is_open for status
            # add .next_close for next close etc ...
            return self._trading_client.get_clock()


    def BUY(self,symbol,qty,tif,side):
        if self.frac != False and symbol['fractionable'] == False: return False
        if self.frac != False: qty = qty / cpr(symbol, self.frac)
        market_order_data = MarketOrderRequest(
            symbol=symbol['ALPACA'],
            qty= qty,
            side=OrderSide.BUY if side == 'LONG' else OrderSide.SELL,
            time_in_force=tif)  # TimeInForce.DAY )
        market_order = self._trading_client.submit_order(order_data=market_order_data)
        self.WRITE_JSON(market_order['client_order_id'], 'SELL')
        return market_order #id=UUID('4a50b5eb-5b16-49a7-a164-a37d69586462') client_order_id='cbd12da1-68da-48bd-b862-a3bd44df6670' created_at=datetime.datetime(2023, 6, 8, 11, 26, 45, 215579, tzinfo=datetime.timezone.utc) updated_at=datetime.datetime(2023, 6, 8, 11, 26, 45, 215579, tzinfo=datetime.timezone.utc) submitted_at=datetime.datetime(2023, 6, 8, 11, 26, 45, 214430, tzinfo=datetime.timezone.utc) filled_at=None expired_at=None canceled_at=None failed_at=None replaced_at=None replaced_by=None replaces=None asset_id=UUID('b0b6dd9d-8b9b-48a9-ba46-b9d54906e415') symbol='AAPL' asset_class=<AssetClass.US_EQUITY: 'us_equity'> notional=None qty='0.056236641' filled_qty='0' filled_avg_price=None order_class=<OrderClass.SIMPLE: 'simple'> order_type=<OrderType.MARKET: 'market'> type=<OrderType.MARKET: 'market'> side=<OrderSide.BUY: 'buy'> time_in_force=<TimeInForce.DAY: 'day'> limit_price=None stop_price=None status=<OrderStatus.ACCEPTED: 'accepted'> extended_hours=False legs=None trail_percent=None trail_price=None hwm=None


    def SELL(self,symbol):
            asset_id = self._trading_client.get_open_position(symbol['ALPACA-POSITION']).asset_id
            x = self._trading_client.close_position(asset_id)
            self.WRITE_JSON(x['client_order_id'],'SELL')
            return x # id=UUID('ad4b62e1-ec8a-472f-bd6b-c5314dd54737') client_order_id='ed71d6c2-6f91-4f7d-a147-2b52cd6b0061' created_at=datetime.datetime(2023, 6, 8, 11, 29, 43, 27936, tzinfo=datetime.timezone.utc) updated_at=datetime.datetime(2023, 6, 8, 11, 29, 43, 27936, tzinfo=datetime.timezone.utc) submitted_at=datetime.datetime(2023, 6, 8, 11, 29, 43, 27379, tzinfo=datetime.timezone.utc) filled_at=None expired_at=None canceled_at=None failed_at=None replaced_at=None replaced_by=None replaces=None asset_id=UUID('8ccae427-5dd0-45b3-b5fe-7ba5e422c766') symbol='TSLA' asset_class=<AssetClass.US_EQUITY: 'us_equity'> notional=None qty='0.48192771' filled_qty='0' filled_avg_price=None order_class=<OrderClass.SIMPLE: 'simple'> order_type=<OrderType.MARKET: 'market'> type=<OrderType.MARKET: 'market'> side=<OrderSide.SELL: 'sell'> time_in_force=<TimeInForce.DAY: 'day'> limit_price=None stop_price=None status=<OrderStatus.ACCEPTED: 'accepted'> extended_hours=False legs=None trail_percent=None trail_price=None hwm=None


    def CHECK_IF_POSITION(self,symbol):
        try:
            return self._trading_client.get_open_position(symbol['ALPACA-POSITION'])
        except:
            return False


    def CHECK_IF_ORDER(self,symbol):
        orders = self._trading_client.get_orders()
        for o in orders:
            o = dict(o)
            if symbol['this'] == o['symbol']:
                return o
        return False


    def CHECK_FULL(self,symbol):
        if symbol['tradable'] == True:
            if self.STATUS().is_open == True:
                if self.CHECK_IF_ORDER(symbol) == False:
                    if self.CHECK_IF_POSITION(symbol) == False:

                        return False # RETURN IF NO POSITION EXISTS

                    else: return self.CHECK_IF_POSITION(symbol) # RETURN IF A POSITION EXISTS
                else:
                    print(f' !!!! ORDER for {symbol["this"]} already exists !!!!')
                    return True
            else:
                stts = self.STATUS()
                print(f'MARKET for {symbol["this"]} is closed, opens in T-{stts.next_open - stts.timestamp}')
                return True
        else:
            print(f'{symbol["this"]} is not TRADEABLE')
            return True


    def OPEN_POSITIONS(self):
        x = self._trading_client.get_all_positions()
        return x


    def OPEN_PL(self):
        positions = self._trading_client.get_all_positions()
        out = []
        pl = 0.0
        for pos in positions:
            out.append({pos.symbol : float(pos.unrealized_pl)})
            pl += float(pos.unrealized_pl)
        return [pl , out]


    def FULL_INFO(self):
        search_params = GetAssetsRequest(asset_class=AssetClass.US_EQUITY)
        assets = self._trading_client.get_all_assets(search_params)
        return assets


    def PORTFOLIO(self,id):
        print(self._trading_client.get_order_by_id(id))


    def WRITE_JSON(self,o_id,side):
        with open(f'STRAT_JSONS/{self.name}.json', 'r') as file:
            self.existing_data = json.load(file)

        self.existing_data['ORDER_IDS'][o_id] = side
        with open(f'STRAT_JSONS/{self.name}.json', 'w') as file:
            json.dump(self.existing_data, file)


"""
paca = ALPACA_BROKER()

#paca.WRITE_JSON(1231244112)

paca.frac = '4h'

paca.CHECK_FULL(TSLA)
"""

















