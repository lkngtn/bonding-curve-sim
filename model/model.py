import random
import math
import mesa

from mesa import Model
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation

from model.agents import RandomTrader

def compute_gini(model):
    agent_wealths = [agent.wealth for agent in model.schedule.agents]
    x = sorted(agent_wealths)
    N = model.num_agents
    B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
    return (1 + (1 / N) - 2 * B)

class BondingCurve(Model):
    '''
        A market model that manages balances of a token and currency pair based on a pricing curve determined by a ratio.
    '''
    def __init__(self, num_agents, token_supply, ratio, agent_starting_currency, agent_belief_sigma, agent_trade_percent):
        super().__init__()
        self.num_agents = num_agents
        self.token_supply = token_supply
        self.ratio = ratio
        self.reserve = self.token_supply * self.ratio

        self.schedule = RandomActivation(self)


        # Instatiate agents
        for i in range(self.num_agents):
            a = RandomTrader(i, self, agent_starting_currency, (self.token_supply/self.num_agents), agent_belief_sigma, agent_trade_percent)
            self.schedule.add(a)
        self.running = True
        self.datacollector = DataCollector(
            model_reporters={"Gini": compute_gini},
            agent_reporters={"Wealth": "wealth"}
        )
        self.datacollector.collect(self)

    def buy(self, amount):
        self.purchase_amount = self.token_supply * ((1 + amount/self.reserve)**self.ratio -1)
        self.token_supply += self.purchase_amount
        self.reserve += amount
        return self.purchase_amount

    def sell(self, amount):
        self.sell_amount = self.reserve * (1 - (1- amount/self.token_supply)**(1/self.ratio))
        self.token_supply -= amount
        self.reserve -= self.sell_amount
        return self.sell_amount

    def current_price(self):
        return self.reserve / (self.token_supply * self.ratio)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

    def run_model(self, n):
        for i in range(n):
            self.step()
