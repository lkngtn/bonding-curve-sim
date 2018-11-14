import numpy as np
from lib.market import Trader


class RandomTrader(Trader):
    '''
    This trader implements a strategy based on a random belief of token value.
    '''
    def __init__(self, unique_id, model, market, currency, tokens):
        super().__init__(unique_id, model, market, currency, tokens)

    def step_strategy(self):
        self.current_price = self.market.current_price()
        self.value_belief = np.random.normal(0, 0.2)

        if self.value_belief < 0 and self.tokens > 0:
            self.sell(self.tokens * abs(self.value_belief))
        elif self.currency > 0:
            self.buy(self.currency * abs(self.value_belief))
