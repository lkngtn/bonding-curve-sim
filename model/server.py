import mesa

#from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter
#from mesa.visualization.modules import TextElement
from mesa.visualization.ModularVisualization import ModularServer
#from mesa.visualization.TextVisualization import TextData
#from mesa.visualization.TextVisualization import TextVisualization

from model.model import BondingCurve

chart1 = ChartModule([
    {"Label": "Gini", "Color": "#56bfdf"}],
    data_collector_name='datacollector',
    canvas_height=300, canvas_width=300
)

server = ModularServer(
    BondingCurve,
    [chart1],
    name="Random Agent Bonding Curve Sim",
    model_params={
        "num_agents": UserSettableParameter('slider', "Number of Agents", 20, 10, 100, 1,
                               description="Choose how many agents to include in the model"),
        "token_supply": UserSettableParameter('slider', "Number of tokens", 40, 10, 400, 1,
                                   description="Choose how many tokens in supply, tokens are split evenly among jurors at initialization."),
        "ratio": UserSettableParameter('slider', "Bonding Curve Reserve Ratio", 0.01, 0.1, 1, 0.01,
                                   description="Constant reserve ration maintained by the bonding curve different values change price function"),
        "agent_belief_sigma": UserSettableParameter('slider', "Agent Belief Sigma", 1, 3, 100, 1,
                                    description="standard deviation for agent beliefs of the true value relative to current price"),
        "agent_starting_currency": UserSettableParameter('slider', "Agent Starting Currency", 1, 3, 100, 1,
                                    description="standard deviation for agent beliefs of the true value relative to current price"),
        "agent_trade_percent": UserSettableParameter('slider', "Agent Trade Percent", 0.05, 0.25, 1, 0.05,
                                    description="standard deviation for agent beliefs of the true value relative to current price")

    })
server.port = 8521
server.launch()
