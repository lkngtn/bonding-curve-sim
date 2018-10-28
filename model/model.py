import random
import math
import mesa
import numpy as np

from mesa import Model
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation

from model.agents import RandomTrader
from lib.gini import gini

def compute_gini(model):
    agent_wealths = np.array([float(agent.wealth) for agent in model.schedule.agents])
    return gini(agent_wealths)

def compute_price(model):
    return model.market.current_price()

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


class RandomMarket(Model):
    '''
        A simulation of random trading behavior against a bonding curve based market.
    '''
    def __init__(self, num_agents, token_supply, ratio, agent_starting_currency, agent_belief_sigma):
        super().__init__()
        self.num_agents = num_agents
        self.market = BondingCurve(token_supply, ratio)

        self.schedule = RandomActivation(self)

        # Instatiate agents
        for i in range(self.num_agents):
            a = RandomTrader(i, self, self.market, agent_starting_currency, (self.market.token_supply/self.num_agents), agent_belief_sigma)
            self.schedule.add(a)
        self.running = True
        self.datacollector = DataCollector(
            model_reporters={"Gini": compute_gini, "Price": compute_price},
            agent_reporters={"Wealth": "wealth"}
        )
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

    def run_model(self, n):
        for i in range(n):
            self.step()
