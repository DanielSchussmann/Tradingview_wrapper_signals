from PACA_Broker import *
from Rating_Class import *


class STRAT():
    def __init__(self):
        self.broker = ALPACA_BROKER()       #broker class from Brokers
        self.rating = INDICATOR_RATING()    #rating class from Rating class
        self.symbols = []
        self.buy_frame= 0
        self.sell_frame = 0
        #STRAT.rating.weights = [i1,i2,i3]
        #STRAT.rating.weights = [1,1,1]
        #STRAT.broker.frac = '4h'

    def buy_logic(self,symbol):
        signal = self.buy_frame(symbol)
        if signal != False:
            self.broker.BUY(signal['symbol'],signal['qty'],signal['tif'],signal['side'])
            return True
        else:
            return False


    def sell_logic(self,symbol,position):
        signal = self.sell_frame(symbol,position.side)
        if signal != False:
            self.broker.SELL(symbol)
            return True
        else:
            return False


    def loop(self,infinite=False):
        while True:
            for symbol in self.symbols:
                position = self.broker.CHECK_FULL(symbol)
                if position == True :
                    continue
                else:
                    try:
                        x = position.side
                        self.sell_logic(symbol,position)

                    except:
                        self.buy_logic(symbol)

            print(f"#### {self.broker.OPEN_PL()} ####")

            if infinite == False: break


