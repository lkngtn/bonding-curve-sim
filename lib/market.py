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

class BondingCurve():
    '''
        A class for bonding curve based token economies
    '''
    def __init__(self, token_supply, ratio):
        self.token_supply = token_supply
        self.ratio = ratio
        self.reserve = self.token_supply * self.ratio

    def buy(self, amount):
        self.purchase_amount = self.token_supply * (((1 + amount/self.reserve)**self.ratio) -1)
        self.token_supply += self.purchase_amount
        self.reserve += amount
        # print("Action Buy -- Reserve: " + str(self.reserve) + " Supply: " + str(self.token_supply) + " Ratio: " + str(self.ratio) + " Price :" + str(self.reserve / (self.token_supply * self.ratio)))
        return self.purchase_amount

    def sell(self, amount):
        self.sell_amount = self.reserve * (1 - (1- amount/self.token_supply)**(1/self.ratio))
        self.token_supply -= amount
        self.reserve -= self.sell_amount
        # print("Action: Sell -- Reserve: " + str(self.reserve) + " Supply: " + str(self.token_supply) + " Ratio: " + str(self.ratio) + " Price :" + str(self.reserve / (self.token_supply * self.ratio)))
        return self.sell_amount

    def current_price(self):
        return self.reserve / (self.token_supply * self.ratio)
