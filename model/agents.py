import numpy as np
from mesa import Agent

class Trader(Agent):
    '''
    The Trader class implements standard actions for an agent to interact with a single currency/token market model.
    '''
    def __init__(self, unique_id, model, market, currency, tokens):
        super().__init__(unique_id, model)
        self.currency = currency
        self.tokens = tokens
        self.wealth = 1
        self.market = market

    def calculate_wealth(self):
        self.wealth = self.currency + (self.tokens * self.market.current_price())

    def buy(self,amount):
        self.tokens += self.market.buy(amount)
        self.currency -= amount

    def sell(self,amount):
        self.tokens -= amount
        self.currency += self.market.sell(amount)

    def skip(self):
        pass

    def step_strategy(self):
        '''
        Implement agent strategy by inheriting class and overwritting this function.
        '''
        self.skip()

    def step(self):
        self.calculate_wealth()
        self.step_strategy()


class RandomTrader(Trader):
    '''
    This trader implements a strategy based on a random belief of token value.
    '''
    def __init__(self, unique_id, model, market, currency, tokens, belief_sigma):
        super().__init__(unique_id, model, market, currency, tokens)
        self.sigma = belief_sigma

    def step_strategy(self):
        self.current_price = self.market.current_price()
        self.value_belief = np.random.normal(0, self.sigma)
        if self.value_belief < 0 and self.tokens > 0:
            self.sell(self.tokens * self.value_belief)
        elif self.currency > 0:
            self.buy(self.currency * self.value_belief)
