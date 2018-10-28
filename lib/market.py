
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
        print("Action Buy -- Reserve: " + str(self.reserve) + " Supply: " + str(self.token_supply) + " Ratio: " + str(self.ratio) + " Price :" + str(self.reserve / (self.token_supply * self.ratio)))
        return self.purchase_amount

    def sell(self, amount):
        self.sell_amount = self.reserve * (1 - (1- amount/self.token_supply)**(1/self.ratio))
        self.token_supply -= amount
        self.reserve -= self.sell_amount
        print("Action: Sell -- Reserve: " + str(self.reserve) + " Supply: " + str(self.token_supply) + " Ratio: " + str(self.ratio) + " Price :" + str(self.reserve / (self.token_supply * self.ratio)))
        return self.sell_amount

    def current_price(self):
        return self.reserve / (self.token_supply * self.ratio)
