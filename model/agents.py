import numpy as np
from mesa import Agent

class Trader(Agent):
    '''
    The Trader class implements standard actions for an agent to interact with a single currency/token market model.
    '''
    def __init__(self, unique_id, model, currency, tokens):
        super().__init__(unique_id, model)
        self.currency = currency
        self.tokens = tokens
        self.wealth = 1

    def calculate_wealth(self):
        self.wealth = self.currency + (self.tokens * self.model.current_price())

    def buy(self,amount):
        self.tokens += self.model.buy(amount)
        self.currency -= amount

    def sell(self,amount):
        self.tokens -= amount
        self.currency += self.model.sell(amount)

    def skip(self):
        pass

    def step_strategy(self):
        '''
        Implement agent strategy by inheriting class and overwritting this function.
        '''
        skip()

    def step(self):
        self.calculate_wealth()
        self.step_strategy()


class RandomTrader(Trader):
    '''
    This trader implements a trading strategy based on a random belief of token value.
    '''
    def __init__(self, unique_id, model, currency, tokens, belief_sigma, trade_percent):
        super().__init__(unique_id, model, currency, tokens)
        self.sigma = belief_sigma
        self.trade_percent = trade_percent

    def step_strategy(self):
        self.current_price = self.model.current_price()
        self.value_beleif = np.random.normal(self.current_price, self.sigma)
        if self.value_beleif < self.current_price and self.tokens > 0:
            self.sell(self.tokens * self.trade_percent)
        elif self.currency > 0:
            self.buy(self.currency*self.trade_percent)
