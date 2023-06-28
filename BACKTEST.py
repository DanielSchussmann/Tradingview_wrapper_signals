import pandas as pd
import numpy as np
#import tensorflow as tf
from dash import dash_table
#from DataPrep import *
import plotly.graph_objects as go
import dash
import json
import datetime
#from strats import *
from symb_LIB.symbol_lib import *

app = dash.Dash(__name__)
server = app.server
app.title = "Backtest"


def get_price(symbol,timestamp,level='close'):
    return float('wherevergetpricefrom(symbol, timestamp , level)')


class BACKTEST_v3():
    def __init__(self): #Innitializing all the required variables
        self.analytics={'orders':[],'portfolio_mvmt': {'ALL':[],'reasons':[]}}
        self.portfolio = 10000
        self.analytics['portfolio_mvmt']['ALL'].append(self.portfolio)
        self.order_size=200
        self.leverage=50
        self.open_orders={}
        self.symbols = []
        self.main_color='#30AC83'
        self.long_text="긴"
        self.short_text='짧은'
        self.column_names=['Hash','StartDate','CloseDate', 'Symbol', 'Type', 'BuyPrice', 'SellPrice', 'Profit', 'Note']

    #NEEDS TO BE CALLED BEFORE STARTING THE PROGRAMM
    def set_symbols(self,symbols=symbol_index): #symbols in form [AAPL,TSLA ... , ]
        for symbol in symbols:
            self.analytics['portfolio_mvmt'][symbol['this']] = []
            self.symbols.append(symbol['this'])


    def MakeOrder(self,timestamp,symbol,o_type,note):
        if o_type != 'LONG' and o_type != 'SHORT':
            raise ValueError('Market execution "{}" is not known to BACKTEST'.format(o_type))

        buy_price = get_price(symbol,timestamp) #np.array(self.data[self.symbols[np.where(self.symbols==symbol)][0]])[self.index][3] # self.symbols[np.where(self.symbols==symbol)][0] ~ 'EURUSD'
                                                                                                        # np.array(self.data['EURUSD'])[0][index][close]
        exe_time=timestamp
        hax=str(uuid.uuid1().hex) #generates a random hash dependent on time. Chance to overlap if there are 100000+ hashes generated at the same time, won't happen so it's fine.
        self.open_orders[hax] = [hax, symbol, o_type, buy_price, exe_time, note]

        print('--Order Executed--')
        return hax


    def SellOrder(self,hax,timestamp):
        buy_price = self.open_orders[hax][3]
        symbol = self.open_orders[hax][1]
        type = self.open_orders[hax][2]
        exe_time = self.open_orders[hax][4]
        note = self.open_orders[hax][5]
        end_time = timestamp

        sell_price = get_price(symbol,timestamp)
        if end_time > exe_time:
            raise ValueError('Sell time is before buy time that not possible my G')

        if type == 'LONG':
            profit = (sell_price-buy_price) * self.order_size * self.leverage
            self.portfolio += (sell_price-buy_price) * self.order_size * self.leverage
            self.analytics['orders'].append([hax, exe_time, end_time, symbol, type, buy_price, sell_price,  profit,note])

        else:
            profit = (buy_price-sell_price) * self.order_size * self.leverage
            self.portfolio += profit
            self.analytics['orders'].append([hax, exe_time, end_time, symbol, type, buy_price, sell_price, profit,note])

        self.analytics['portfolio_mvmt'][symbol].append(self.portfolio)
        self.analytics['portfolio_mvmt']['ALL'].append(self.portfolio)

        self.analytics[symbol].append([hax, exe_time, end_time, symbol, type, buy_price, sell_price, profit, note])
        del self.open_orders[hax]



    def _write_to_json(self,title):
        with open(title, 'w', encoding='utf-8') as f:
            json.dump(self.analytics, f, ensure_ascii=False, indent=4)


#VISUALIZATION OF THEM DATA TINGS
    def _annotations(self, X):
        return [dict(
                        name=self.analytics[X][i][0],
                        x=self.analytics[X][i][1],
                        y=self.analytics[X][i][5],
                        text=self.long_text if self.analytics[X][i][4]=='LONG' else self.short_text,
                        clicktoshow='onoff',
                        showarrow=True,
                        arrowcolor='#057FA6' if self.analytics[X][i][4]=='LONG' else 'coral',
                        arrowhead=1,arrowwidth=2,
                        arrowsize=1,
                        opacity=0.4,
                        ax=0,
                        hovertext=str(self.analytics[X][i][1])+' / '+str(self.analytics[X][i][0]),
                        ay=30 if self.analytics[X][i][4]=='LONG' else -30 ,
                        font_color='white',
                        bgcolor='#057FA6' if self.analytics[X][i][4]=='LONG' else 'coral') for i in range(len(self.analytics[X]))]


    def _candel_plot(self,symbol):

        """
        Something something Symbol
        data = Financial data from self.draw_start  to self.draw_end
        """

        data = {'Open':[self.draw_start - self.draw_end],'High':[self.draw_start - self.draw_end],'Low':[self.draw_start - self.draw_end],'Close':[self.draw_start - self.draw_end]}

        if len(self.analytics[symbol]) != 0:
            return go.Candlestick(
                            increasing_line_color='rgba(44, 104, 82, 1)', increasing_fillcolor='rgba(44, 104, 82, 1)',
                            decreasing_line_color='rgba(115, 0, 0, 1)', decreasing_fillcolor='rgba(115, 0, 0, 1)',
                            open=data['Open'],
                            high=data['High'],
                            low=data['Low'],
                            close=data['Close'], name=symbol, opacity=0.8)
        else:
            return go.Candlestick(
                            increasing_line_color='#DAFFF3', increasing_fillcolor='#DAFFF3',
                            decreasing_line_color='#DAFFF3', decreasing_fillcolor='#DAFFF3',
                            open=data['Open'],
                            high=data['High'],
                            low=data['Low'],
                            close=data['Close'], name=symbol, opacity=0.8)


    def _draw(self):
        fig_load = go.Figure(data=[])

        # fig_acc.update_layout(hoverlabel=dict(bgcolor="white", font_size=16, font_family="Arial"),color_discrete_sequence=plotly.colors.sequential.RdBu)#accuracy of the bot in total also in regards to single currency
        DropDown_options = [[{'label': self.symbols[i], 'value': self.symbols[i]}][0] for i in range(len(self.symbols))]
        DropDown_options.append({'label': 'ALL', 'value': 'ALL'})

        app.layout = dash.html.Div([

            dash.html.H1(children='BACKTESTING SUMMARY',
                         style={'textAlign': 'center', 'font-size': '40px', 'margin-bottom': '20px'}),

            dash.html.Div([
                dash.html.Div(
                    [dash.dcc.Graph(id="portfolio", figure=fig_load, style={'height': '60vh', 'width': '60vw'})],
                    style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'flex-start',
                           'align-items': 'space-around', 'box-shadow': 'rgba(100, 100, 111, 0.2) 0px 7px 29px 0px'}),
                dash.dcc.Graph(id="accuracy", figure=fig_load,
                               style={'height': '60vh', 'padding': '0px', 'border-radius': '10px',
                                      'box-shadow': 'rgba(100, 100, 111, 0.2) 0px 7px 29px 0px'}), ],
                id='top_row', style={'display': 'flex', 'flex-direction': 'row', 'justify-content': 'space-around',
                                     'align-items': 'center', 'margin-bottom': '25px', }),

            dash.html.Div([
                dash.dcc.Graph(id='F_O_V', figure=fig_load, style={'width': '100%', 'height': '85vh'}),
                dash_table.DataTable(
                    id='table',
                    columns=([{'name': 'Hash', 'id': 'Hash', 'type': 'any'},
                              {'name': 'StartId', 'id': 'StartId', 'type': 'any'},
                              {'name': 'CloseId', 'id': 'CloseId', 'type': 'any'},
                              {'name': 'Symbol', 'id': 'Symbol', 'type': 'any'},
                              {'name': 'Type', 'id': 'Type', 'type': 'any'},
                              {'name': 'BuyPrice', 'id': 'BuyPrice', 'type': 'any'},
                              {'name': 'SellPrice', 'id': 'SellPrice', 'type': 'any'},
                              {'name': 'Profit', 'id': 'Profit', 'type': 'any'},
                              {'name': 'Note', 'id': 'Note', 'type': 'any'}]), style_cell={'textAlign': 'left'},
                    data=pd.DataFrame(self.analytics['orders'], columns=self.column_names).to_dict('records'),
                    editable=False)],
                style={'fontsize': '30px', 'margin-bottom': '5px', 'width': '95.5vw',
                       'box-shadow': 'rgba(100, 100, 111, 0.2) 0px 7px 29px 0px', 'align-self': 'center'}),

            dash.dcc.Dropdown(id='options',
                              options=DropDown_options,
                              value='ALL',
                              style={'width': '20vw', 'position': 'fixed'})],
            style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'flex-start',
                   'align-items': 'space-around', 'padding': '0px', 'margin': '0px'})

        @app.callback(dash.Output('portfolio', 'figure'), dash.Output('accuracy', 'figure'),
                      dash.Output('F_O_V', 'figure'), dash.Output('table', 'data'), [dash.Input('options', 'value')])
        def update_figure(value):
            if value == 'ALL':
                fig_ALL = go.Figure(data=[self._candel_plot(self.symbols[i]) for i in range(len(self.symbols))],
                                    layout_title_text='Full Chart and Transaction list')
                fig_ALL.update_layout(xaxis_rangeslider_visible=False, template='simple_white')

                fig_port = go.Figure(data=[go.Scatter(x=np.arange(0, len(self.analytics['portfolio_mvmt'][value])),
                                                      y=self.analytics['portfolio_mvmt'][value])],
                                     layout_title_text='Portfolio Evolution')
                fig_port.update_layout(template='simple_white', hovermode="x",
                                       hoverlabel=dict(bgcolor="#636EFA", font_color='white', font_size=16,
                                                       font_family="Arial"), yaxis_tickprefix='€',
                                       yaxis_tickformat=',.2f')

                fig_acc = go.Figure(data=[go.Pie(
                    values=[np.count_nonzero(np.transpose(self.analytics['orders'])[7].astype('float32') < 0),
                            np.count_nonzero(np.transpose(self.analytics['orders'])[7].astype('float32') > 0)],
                    labels=['un-Profitable', 'Profitable'], hole=0.4, marker_colors=['#F3BCAF', '#AFF3D4'])],
                    layout_title_text='Trade Count')
                fig_acc.update_traces(hoverinfo='label+value', hoverlabel=dict(font_size=26, font_family="Arial"))
                fig_acc.update_layout(
                    annotations=[dict(text=len(self.analytics['orders']), x=0.5, y=0.5, font_size=50, showarrow=False)])

                return fig_port, fig_acc, fig_ALL, pd.DataFrame(self.analytics['orders'],
                                                                columns=self.column_names).to_dict('records')

            if value != 'ALL':
                fig_out = go.Figure(data=[self._candel_plot(value)],
                                    layout_title_text='{} Chart and Transaction list'.format(value))
                fig_out.update_layout(xaxis_rangeslider_visible=False, template='simple_white',
                                      annotations=self._annotations(value))

                fig_port = go.Figure(data=[go.Scatter(x=np.arange(0, len(self.analytics['portfolio_mvmt'][value])),
                                                      y=self.analytics['portfolio_mvmt'][value])],
                                     layout_title_text='Portfolio Evolution')
                fig_port.update_layout(template='simple_white', hovermode="x",
                                       hoverlabel=dict(bgcolor="#636EFA", font_color='white', font_size=16,
                                                       font_family="Arial"), yaxis_tickprefix='€',
                                       yaxis_tickformat=',.2f')

                fig_acc = go.Figure(data=[go.Pie(
                    values=[np.count_nonzero(np.transpose(self.analytics[value])[7].astype('float32') < 0),
                            np.count_nonzero(np.transpose(self.analytics[value])[7].astype('float32') > 0)],
                    labels=['un-Profitable', 'Profitable'], hole=0.4, marker_colors=['#F3BCAF', '#AFF3D4'])],
                    layout_title_text='Trade Count')
                fig_acc.update_traces(hoverinfo='label+value', hoverlabel=dict(font_size=26, font_family="Arial"))
                fig_acc.update_layout(
                    annotations=[dict(text=len(self.analytics[value]), x=0.5, y=0.5, font_size=50, showarrow=False)])

                return fig_port, fig_acc, fig_out, pd.DataFrame(self.analytics[value],
                                                                columns=self.column_names).to_dict('records')

        if __name__ == '__main__':
            app.run_server(debug=True)

    def finalize(self, title):
        self.draw_start = self.analytics['orders'][0][1]
        self.draw_end = self.analytics['orders'][-1][2]


        self._write_to_json(title)
        self._draw()


standard_deviation=lambda data: np.sum(((data-(np.mean(data)))**2)/len(data))**0.5 #usage example: st_de_rolling([2,4,4,4,5,5,7,9]) => 2


rando = BACKTEST_v3()

rando.set_symbols()
start_date = datetime.date(2022, 4, 1)  # Start date
end_date = datetime.date(2023, 4, 15)  # End date




for single_date in range((end_date - start_date).days + 1):
    current_date = start_date + datetime.timedelta(days=single_date)


    for symbol in rando.symbols:
        d = np.array([np.random.rand(), np.random.rand()], dtype=float)
        std_break=True
        decision = 'np.array((std_break, d), dtype=object)'

        #LONG
        if d[0] > d[1] and std_break :
            get_hash_if_need = rando.MakeOrder(current_date, symbol, 'LONG', str(decision))

        #SHORT
        elif d[0] < d[1] and std_break  :
            rando.MakeOrder(current_date, symbol, 'SHORT',str(decision))




    #CHECK IF SELL ARGUMENT IS APPLICABLE
    for order in rando.open_orders:
        order_details = rando.open_orders[order]

        if 'SELL LOGIC':

            rando.SellOrder(order,current_date)




#print(dis.analytics)

#dis.init_layout()
rando.finalize('test.json')






#Harmonic Pattern strategy
"""
harm=BACKTEST_v3()
[harm.tick() for x in range(0,50)]

my_orders=[]

x=0
while x < 600:
    for s in range(len(harm.symbols)):
            data_read=harm.data[harm.symbols[s]][harm.index-15:harm.index]
            Crab = XABCD_fixed_bull(data_read, [[0.382, 0.618], [0.382, 0.886], [2.24, 3.618], [1.6175, 1.6185]])
            Gartley = XABCD_fixed_bull(data_read, [[0.6175, 0.6185], [0.382, 0.886], [1.13, 1.618], [0.7855, 0.7865]])
            Bat = XABCD_fixed_bull(data_read, [[0.382, 0.500], [0.382, 0.886], [1.618, 2.618], [0.8855, 0.8865]])
            Butterfly = XABCD_fixed_bull(data_read, [[0.7855, 0.7865], [0.382, 0.886], [1.618, 2.24], [1.265, 1.272]])

            if len(Crab) !=0:
                typ='LONG' if Crab[-1][1][0] > Crab[-1][1][1] else 'SHORT'
                xxx = harm.MakeOrder(harm.symbols[s], typ, 'Crab')
                my_orders.append(xxx)
                x+=14

            elif len(Gartley) !=0:
                typ= 'LONG' if Gartley[-1][1][0] > Gartley[-1][1][1] else 'SHORT'
                xxx = harm.MakeOrder(harm.symbols[s],typ, 'Gart')
                my_orders.append(xxx)
                x += 14

            elif len(Bat) !=0:
                typ= 'LONG' if Bat[-1][1][0] > Bat[-1][1][1] else 'SHORT'
                xxx = harm.MakeOrder(harm.symbols[s], typ, 'Bat')
                my_orders.append(xxx)
                x += 14

            elif len(Butterfly) != 0:
                typ='LONG' if Butterfly[-1][1][0] > Butterfly[-1][1][1] else 'SHORT'
                xxx = harm.MakeOrder(harm.symbols[s], typ, 'Butterfly')
                my_orders.append(xxx)
                x += 14

    o = 0
    while o < len(my_orders):
        if harm.open_orders[my_orders[o]][4] + 10 < harm.index:
            harm.SellOrder(my_orders[o])
            my_orders.pop(o)
        o += 1
    x+=1
    harm.tick()




harm.init_layout()
harm.draw()
"""
#with open('Example1.json', 'w', encoding='utf-8') as f:
 #   json.dump(harm.analytics, f, ensure_ascii=False, indent=4)



"""


dis = BACKTEST_v3()


[dis.tick() for x in range(0,30)]
standard_deviation=lambda data: np.sum(((data-(np.mean(data)))**2)/len(data))**0.5
my_orders=[]


pred = tf.keras.models.load_model('Neural_Networks/promise_1')
for x in range(0,1000):
    prediction_data=[]
    for f in range(len(dis.symbols)):
       prediction_data.append(np.array(normalize([ dis.data[dis.symbols[f]]['Close'][x]/dis.data[dis.symbols[f]]['Close'][dis.index] for x in range(dis.index - 10,dis.index)])))

    prediction_data=np.asarray(prediction_data)
    #print(prediction_data)
    #prediction = pred.predict_on_batch(prediction_data_1)
    prdctn= pred.predict_on_batch(prediction_data)
    #print(prdctn)
    for t in range(len(dis.symbols)):
       #print(np.where(np.amax(prdctn[t]))[0][0])
       if np.where(np.amax(prdctn[t]))[0][0] == 1:
            continue
       elif np.where(np.amax(prdctn[t]))[0][0] == 0:
           xxx = dis.MakeOrder(dis.symbols[t], 'LONG',str(prdctn[t]))
           my_orders.append(xxx)
       elif np.where(np.amax(prdctn[t]))[0][0] ==2:
           xxx = dis.MakeOrder(dis.symbols[t], 'SHORT',str(prdctn[t]))
           my_orders.append(xxx)


    o = 0
    while o<len(my_orders):
        #print(dis.open_orders[my_orders[o]])
        if dis.open_orders[my_orders[o]][4] + 5 < dis.index:
            dis.SellOrder(my_orders[o])
            my_orders.pop(o)
        o += 1
    dis.tick()
#print(dis.analytics)

#dis.init_layout()
#dis.draw()
with open('Example1.json', 'w', encoding='utf-8') as f:
    json.dump(dis.analytics, f, ensure_ascii=False, indent=4)

"""
########## ############################--------------------------------------------------------------------------------------








"""




class BACKTEST_v2():
    def __init__(self): #Innitializing all the required variables
        self.analytics={'orders':[],'portfolio_mvmt':[],'EURUSD':[],'EURAUD':[],'EURJPY':[],'EURGBP':[],'EURCHF':[],'reasons':[]}
        self.portfolio = 10000
        self.analytics['portfolio_mvmt'].append(self.portfolio)
        self.order_size=200
        self.leverage=50
        self.index=0
        self.data=load_data.copy()
        self.ea = self.data['EURAUD']
        self.ec = self.data['EURCHF']
        self.eg = self.data['EURGBP']
        self.ej = self.data['EURJPY']
        self.eu = self.data['EURUSD']
        self.draw_data=0
        self.open_orders={}
        self.break_index=15


    def tick(self): #tick reffers to receiving a new candle from the market
        self.index+=1



    def MakeOrder(self,symbol,type):
        if symbol =='EURAUD':
                buy_price = np.array(self.ea)[self.index][3]
        elif symbol =='EURCHF':
                buy_price = np.array(self.ec)[self.index][3]
        elif symbol =='EURGBP':
                buy_price = np.array(self.eg)[self.index][3]
        elif symbol =='EURJPY':
                buy_price = np.array(self.ej)[self.index][3]
        elif symbol =='EURUSD':
                buy_price = np.array(self.eu)[self.index][3]
        else:
            raise ValueError('Symbol "{}" is not known to BACKTEST'.format(symbol))

        if type!='LONG' and type!='SHORT':
            raise ValueError('Market execution "{}" is not known to BACKTEST'.format(type))

        exe_id=self.index
        hax=str(uuid.uuid1().hex) #generates a random hash dependent on time. Chance to overlap if there are 100000+ hashes generated at the same time, won't happen so it's fine.
        self.open_orders[hax] = [hax, symbol, type, buy_price, exe_id]
        #self.analytics[hax] = [symbol, type,buy_price, exe_id]
        return hax


    def SellOrder(self,hax):
        buy_price = self.open_orders[hax][3]
        symbol = self.open_orders[hax][1]
        type = self.open_orders[hax][2]
        exe_id = self.open_orders[hax][4]
        end_id = self.index
        if symbol == 'EURAUD':
            sell_price= np.array(self.ea)[self.index][3]
        elif symbol == 'EURCHF':
            sell_price = np.array(self.ec)[self.index][3]
        elif symbol == 'EURGBP':
            sell_price = np.array(self.eg)[self.index][3]
        elif symbol == 'EURJPY':
            sell_price = np.array(self.ej)[self.index][3]
        elif symbol == 'EURUSD':
            sell_price = np.array(self.eu)[self.index][3]
        else:
            raise ValueError('How the hell did "{}" end up here??'.format(symbol))

        if type == 'LONG':
            profit = (sell_price-buy_price) * self.order_size * self.leverage
            self.portfolio += (sell_price-buy_price) * self.order_size * self.leverage
            self.analytics['orders'].append([hax, exe_id, end_id, symbol, type, buy_price, sell_price, 'fail']) if profit < 0 else self.analytics['orders'].append([hax, exe_id, end_id, symbol, type, buy_price, sell_price, 'succ'])

        else:
            profit = (buy_price-sell_price) * self.order_size * self.leverage
            self.portfolio += profit
            self.analytics['orders'].append([hax, exe_id, end_id, symbol, type, buy_price, sell_price, 'fail']) if profit<0 else self.analytics['orders'].append([hax, exe_id, end_id, symbol, type, buy_price, sell_price, 'succ'])
        self.analytics['portfolio_mvmt'].append(self.portfolio)

        self.analytics[symbol].append([hax, exe_id, end_id, type, buy_price, sell_price])
        del self.open_orders[hax]



#####################################--------------------------------------------------------------------------------------

class VIZ():
    def __init__(self):
        self.data=load_data
        self.leng=1000
        self.main_color='#30AC83'
        self.order_history=0
        self.analytics={}
        self.addon= {'EURUSD': {'Shape':[],'Scatter':[]} ,'EURAUD':{'Shape':[],'Scatter':[]},'EURJPY':{'Shape':[],'Scatter':[]},'EURGBP':{'Shape':[],'Scatter':[]},'EURCHF':{'Shape':[],'Scatter':[]}}
    def annotations(self, X):
        return [dict(
                        name=self.analytics[X][i][0],
                        x=self.analytics[X][i][1],
                        y=self.analytics[X][i][4],
                        text="긴" if self.analytics[X][i][3]=='LONG' else '짧은',
                        clicktoshow='onoff',
                        showarrow=True,
                        arrowcolor='#057FA6' if self.analytics[X][i][3]=='LONG' else 'coral',
                        arrowhead=1,arrowwidth=2,
                        arrowsize=1,
                        opacity=0.4,
                        ax=0,
                        hovertext=str(self.analytics[X][i][1])+' / '+str(self.analytics[X][i][0]),
                        ay=30 if self.analytics[X][i][3]=='LONG' else -30 ,
                        font_color='white',
                        bgcolor='#057FA6' if self.analytics[X][i][3]=='LONG' else 'coral') for i in range(len(self.analytics[X]))]

    def internal_plot(self,PLOT,symbol,plot_type):
        self.addon[symbol][plot_type].append(PLOT)



    def candel_plot(self,X):
        if len(self.analytics[X]) != 0:
            return go.Candlestick(
                            increasing_line_color='rgba(44, 104, 82, 1)', increasing_fillcolor='rgba(44, 104, 82, 1)',
                            decreasing_line_color='rgba(115, 0, 0, 1)', decreasing_fillcolor='rgba(115, 0, 0, 1)',
                            open=self.data[X]['Open'],
                            high=self.data[X]['High'],
                            low=self.data[X]['Low'],
                            close=self.data[X]['Close'], name=X, opacity=0.8)
        else:
            return go.Candlestick(
                            increasing_line_color='#DAFFF3', increasing_fillcolor='#DAFFF3',
                            decreasing_line_color='#DAFFF3', decreasing_fillcolor='#DAFFF3',
                            open=self.data[X]['Open'],
                            high=self.data[X]['High'],
                            low=self.data[X]['Low'],
                            close=self.data[X]['Close'], name=X, opacity=0.8)

    def init_layout(self):
        self.fig_ALL = go.Figure(data=[self.candel_plot('EURUSD'),self.candel_plot('EURGBP'),self.candel_plot('EURJPY'),self.candel_plot('EURCHF'),self.candel_plot('EURAUD')],layout_title_text='Chart and Transaction list')
        self.fig_ALL.update_layout(xaxis_rangeslider_visible=False,template='simple_white')

        self.fig_EURUSD = go.Figure(data=[self.candel_plot('EURUSD')])
        self.fig_EURUSD.update_layout(xaxis_rangeslider_visible=False, template='simple_white', annotations=self.annotations('EURUSD'))

        #[fig_EURUSD.add_shape(self.addon['EURUSD']['Scatter'][an]) for an in range(len(self.addon['EURUSD']['Scatter']))]


        self.fig_EURGBP = go.Figure(data=[self.candel_plot('EURGBP')])
        self.fig_EURGBP.update_layout(xaxis_rangeslider_visible=False, template='simple_white', annotations=self.annotations('EURGBP'))

        self.fig_EURJPY = go.Figure(data=[self.candel_plot('EURJPY')])
        self.fig_EURJPY.update_layout(xaxis_rangeslider_visible=False, template='simple_white', annotations=self.annotations('EURJPY'))

        self.fig_EURCHF = go.Figure(data=[self.candel_plot('EURCHF')])
        self.fig_EURCHF.update_layout(xaxis_rangeslider_visible=False, template='simple_white', annotations=self.annotations('EURCHF'))

        self.fig_EURAUD = go.Figure(data=[self.candel_plot('EURAUD')])
        self.fig_EURAUD.update_layout(xaxis_rangeslider_visible=False, template='simple_white', annotations=self.annotations('EURAUD'))

        self.fig_port =go.Figure(data=[go.Scatter(x=np.arange(0, len(self.analytics['portfolio_mvmt'])), y=self.analytics['portfolio_mvmt'] )],layout_title_text='Portfolio Evolution')
        self.fig_port.update_layout(template='simple_white',hovermode="x",hoverlabel=dict(bgcolor="#636EFA", font_color='white', font_size=16, font_family="Arial"),yaxis_tickprefix = '$', yaxis_tickformat = ',.2f')

        self.fig_acc = go.Figure(data=[go.Pie(values=[np.count_nonzero(np.transpose(self.analytics['orders'])[-1]=='succ'), np.count_nonzero(np.transpose(self.analytics['orders'])[-1]=='fail'), 0], labels=['Succ', 'Fail', 'Random'], hole=0.4,marker_colors=['#4824BA','#BB4C71','#FFCFE1'])],layout_title_text='Trade Count')
        self.fig_acc.update_traces(hoverinfo='label+value',hoverlabel=dict(font_size=26, font_family="Arial"))
        self.fig_acc.update_layout(annotations=[dict(text=len(self.analytics['orders']), x=0.5, y=0.5, font_size=50, showarrow=False)])

    def draw(self):
        app = dash.Dash(__name__)
        app.title = "Backtest"
        #fig_acc.update_layout(hoverlabel=dict(bgcolor="white", font_size=16, font_family="Arial"),color_discrete_sequence=plotly.colors.sequential.RdBu)#accuracy of the bot in total also in regards to single currency
        app.layout = dash.html.Div([
                dash.html.H1(children='BACKTESTING SUMMARY', style={'textAlign': 'center', 'font-size':'40px','margin-bottom': '20px'}),

                dash.html.Div([
                    dash.html.Div([
                        #dash.html.H4(children='Portfolio Evolution',style={'textAlign': 'center', 'font-size': '25px', 'font-style':'italic','background-color':'red'}),
                        dash.dcc.Graph(id="portfolio",figure=self.fig_port, style={'height': '60vh','width':'60vw'}),
                    ], style={'display':'flex','flex-direction': 'column','justify-content':'flex-start','align-items':'space-around','box-shadow':'rgba(100, 100, 111, 0.2) 0px 7px 29px 0px'}),
                    dash.dcc.Graph(id="accuracy", figure=self.fig_acc, style={'height': '60vh','padding':'0px','border-radius':'10px','box-shadow':'rgba(100, 100, 111, 0.2) 0px 7px 29px 0px'}),
                ], id='top_row',style={'display':'flex','flex-direction': 'row','justify-content':'space-around','align-items':'center','margin-bottom': '25px',}),

                dash.html.Div([
                    dash.dcc.Graph(id='F_O_V', figure=self.fig_ALL,style={ 'width': '100%', 'height': '85vh'}),
                    dash_table.DataTable(
                    id='table',
                    columns=([{'name':'Hash', 'id':'Hash','type':'any'},
                              {'name': 'StartId', 'id': 'StartId', 'type': 'any'},
                              {'name':'CloseId', 'id':'CloseId','type':'any'},
                              {'name': 'Type', 'id': 'Type', 'type': 'any'},
                              {'name':'BuyPrice', 'id':'BuyPrice','type':'any'},
                              {'name':'SellPrice', 'id':'SellPrice','type':'any'}]),style_cell={'textAlign': 'left'},
                    data=pd.DataFrame(self.analytics['EURUSD'],columns=['Hash','StartId','Type', 'CloseId', 'BuyPrice', 'SellPrice']).to_dict('records'),
                    editable=False)
                ], style={'fontsize': '30px', 'margin-bottom': '5px', 'width': '95.5vw','box-shadow': 'rgba(100, 100, 111, 0.2) 0px 7px 29px 0px', 'align-self': 'center'}),
            dash.dcc.Dropdown(id='options',
                              options=[{'label': 'ALL', 'value': 'ALL'},
                                       {'label': 'EURUSD', 'value': 'EURUSD'},
                                       {'label': 'EURGBP', 'value': 'EURGBP'},
                                       {'label': 'EURJPY', 'value': 'EURJPY'},
                                       {'label': 'EURCHF', 'value': 'EURCHF'},
                                       {'label': 'EURAUD', 'value': 'EURAUD'},
                                       ], value='ALL', style={'width': '20vw', 'position': 'fixed'}
                              ),
        ],style={'display':'flex','flex-direction': 'column','justify-content':'flex-start','align-items':'space-around','padding':'0px','margin':'0px'})



        @app.callback(dash.Output('F_O_V', 'figure'), dash.Output('table','data'), [dash.Input('options', 'value')])
        def update_figure(value):
            if value == 'EURUSD':
                return self.fig_EURUSD, pd.DataFrame(self.analytics['EURUSD'], columns=['Hash', 'StartId', 'CloseId', 'Type','BuyPrice', 'SellPrice']).to_dict('records')
            if value == 'EURGBP':
                return self.fig_EURGBP, pd.DataFrame(self.analytics['EURGBP'], columns=['Hash', 'StartId', 'CloseId','Type', 'BuyPrice', 'SellPrice']).to_dict('records')
            if value == 'EURJPY':
                return self.fig_EURJPY, pd.DataFrame(self.analytics['EURJPY'], columns=['Hash', 'StartId', 'CloseId','Type', 'BuyPrice', 'SellPrice']).to_dict('records')
            if value == 'EURCHF':
                return self.fig_EURCHF, pd.DataFrame(self.analytics['EURCHF'], columns=['Hash', 'StartId', 'CloseId', 'Type','BuyPrice', 'SellPrice']).to_dict('records')
            if value == 'EURAUD':
                return self.fig_EURAUD, pd.DataFrame(self.analytics['EURAUD'], columns=['Hash', 'StartId', 'CloseId','Type', 'BuyPrice', 'SellPrice']).to_dict('records')
            if value == 'ALL':
                return self.fig_ALL, pd.DataFrame([self.analytics['EURUSD']], columns=['Hash', 'StartId', 'CloseId','Type', 'BuyPrice', 'SellPrice']).to_dict('records')


        if __name__ == '__main__':
                app.run_server(debug=True)


dis = BACKTEST_v2()
vis = VIZ()

[dis.tick() for x in range(0,30)]
standard_deviation=lambda data: np.sum(((data-(np.mean(data)))**2)/len(data))**0.5
my_orders=[]
symbols = [[dis.ea,'EURAUD'],[dis.eg,'EURGBP'],[dis.ej,'EURJPY'],[dis.eu,'EURUSD'],[dis.ec,'EURCHF']]


for j in range(30,global_deli-30):

    if j%20==0:

#Check for inn
        for s in range(0,len(symbols)):
            cur_candel = np.array(symbols[s][0])[dis.index]
            cur_close = cur_candel[3]
            rng = np.array(symbols[s][0])[dis.index-20:dis.index]
            cur_mean = np.mean(rng)
            cur_deviation = standard_deviation(rng)
            #print(rng,cur_deviation,cur_mean)
            #print(symbols[s][1],cur_candel,cur_deviation,cur_mean,dis.index)
            if  cur_candel.any() < cur_mean - cur_deviation:
                xxx = dis.MakeOrder(symbols[s][1], 'SHORT')
                my_orders.append(xxx)
            if cur_mean + cur_deviation < cur_candel.any():
                xxx = dis.MakeOrder(symbols[s][1], 'LONG')
                my_orders.append(xxx)


#check for exit condition
    o = 0
    while o<len(my_orders):
        #print(dis.open_orders[my_orders[o]])
        if dis.open_orders[my_orders[o]][4] + 5 < dis.index:
            dis.SellOrder(my_orders[o])
            my_orders.pop(o)
        o += 1
    dis.tick()
"""
"""

#vis = VIZ()
#vis.analytics = dis.analytics
#vis.order_history = pd.DataFrame.from_dict(dis.open_orders, orient='index', columns=['Hash', 'Symbol', 'OrderType', 'BuyPrice', 'Index'])
#vis.init_layout()
#is.internal_plot(go.Scatter(x=[1,2,3],y=[1,1,1]),'EURUSD','Shape')
#vis.draw()



























































"""