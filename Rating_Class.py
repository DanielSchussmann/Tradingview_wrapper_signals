import numpy as np



# INDICATOR RATINGS 0 = sell 1 = buy
class INDICATOR_RATING():
    def __init__(self):
        self.info_data = {}
        self.absolute_rating = 0
        self.weighted_rating = 0
        self.absolute_spread = 0
        self.weighted_spread = 0
        self.indicator_values_absolute = []
        self.indicator_values_weighted = []
        self.symbol = 'NAN'
        self.weights = []
        self.indicators = []
        self.parameters = []

    def get_rating(self, symbol):  # weight 1 will correlate to function 1
        # <--------------------------CHEKC-IF-SETUP-IS-CORRECT------------------------------------------------------------------------------------>
        if len(self.indicators) != len(self.weights): raise Exception(
            'every indicator needs an associated weight aka |indicatos| == |weights|')
        if len(self.indicators) == 0 or len(self.weights) == 0: raise Exception(
            'both indicatos and weights need to assigned')

        # <-------------------------PAIRWISE-SUBTRACTION-FUNCTION------------------------------------------------------------------------------------------------------->
        pair_wise_subtraction = lambda values: np.concatenate([list(abs(np.array(values) - i_value))[count:] for i_value, count in zip(values, range(1, len(values)))])

        # <--------------------------CREATE-LIST-OF-INSERTED-INDICATOR-FUNCTIONS------------------------------------------------>
        self.indicator_values_absolute = [indicator(symbol) for indicator in self.indicators]
        self.indicator_values_weighted = [indicator(symbol) * weight for indicator, weight in zip(self.indicators, self.weights)]

        # <--------------------------CALCULATE-THE-RATINGS-AND-SPREADS-------------------------------->
        self.absolute_rating = np.average(self.indicator_values_absolute)
        self.weighted_rating = np.average(self.indicator_values_weighted)
        self.absolute_spread = np.average(pair_wise_subtraction(self.indicator_values_absolute))
        self.weighted_spread = np.average(pair_wise_subtraction(self.indicator_values_weighted))

        # <--------------------------COLLECT-ALL-DATA-INTO-A-SINGLE-OUTPUT----------------->
        self.info_data['absolute-rating'] = self.absolute_rating
        self.info_data['weighted-rating'] = self.weighted_rating
        self.info_data['absolute-spread'] = self.absolute_spread
        self.info_data['weighted-spread'] = self.weighted_spread
        self.info_data['indicator-list-absolute'] = self.indicator_values_absolute
        self.info_data['indicator-list-weighted'] = self.indicator_values_weighted
        self.info_data['indicators'] = self.indicators




"""
test = INDICATOR_RATING()

test.indicators = [TV_indicators, news_BLOB]

test.weights = [1, 0.5]

test.get_rating(AAPL)

print(test.info_data)
"""