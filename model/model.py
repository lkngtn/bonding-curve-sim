import random
import math
import mesa
import numpy as np

from mesa import Model
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation

from model.agents import RandomTrader
from lib.gini import gini
from lib.market import BondingCurve

def compute_gini(model):
    agent_wealths = np.array([float(agent.wealth) for agent in model.schedule.agents])
    return gini(agent_wealths)

def compute_cumulative_wealth(model):
    return sum([agent.wealth for agent in model.schedule.agents])

def compute_currency_supply(model):
    return sum([agent.currency for agent in model.schedule.agents]) + model.market.reserve

def compute_price(model):
    return model.market.current_price()

def compute_token_supply(model):
    return model.market.token_supply

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
            model_reporters={"Gini": compute_gini, "Price": compute_price, "Token_Supply": compute_token_supply, "Currency_Supply": compute_currency_supply, "Total_Wealth": compute_cumulative_wealth},
            agent_reporters={"Wealth": "wealth"}
        )
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        print("Gini: " + str(compute_gini(self)))
        print("Total Wealth: " + str(compute_cumulative_wealth(self)))
        print("Currency Supply: " + str(compute_currency_supply(self)))
        print("Token Supply: " + str(compute_token_supply(self)))
        self.datacollector.collect(self)

    def run_model(self, n):
        for i in range(n):
            self.step()
