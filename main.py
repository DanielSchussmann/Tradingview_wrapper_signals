from symb_LIB.symbol_lib import *
from INDICATORS import *
import json
import datetime



#<-------------------------------ACCURACY-TESTING------------------------------->
testing_symbols = [AAPL,TSLA,IBM,PFE]
testing_frames = ['1W','1d','1h']

for symb in testing_symbols:
    for frm in testing_frames:
        search = TV_indicators(symb, frm)

        with open('data.json') as d:
            file = json.load(d)

        file[symb['this']][frm][str(datetime.datetime.now())[:16]] = search

        with open('data.json', 'w') as json_file:
            json.dump(file, json_file)






