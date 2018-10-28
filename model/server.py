import mesa

#from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter
#from mesa.visualization.modules import TextElement
from mesa.visualization.ModularVisualization import ModularServer
#from mesa.visualization.TextVisualization import TextData
#from mesa.visualization.TextVisualization import TextVisualization

from model.model import RandomMarket

chart1 = ChartModule([
    {"Label": "Gini", "Color": "#56bfdf"}],
    data_collector_name='datacollector',
    canvas_height=300, canvas_width=300
)

chart2 = ChartModule([
    {"Label": "Price", "Color": "#56bfdf"}],
    data_collector_name='datacollector',
    canvas_height=300, canvas_width=300
)


server = ModularServer(
    RandomMarket,
    [chart1,chart2],
    name="Random Agent Bonding Curve Sim",
    model_params={
        "num_agents": UserSettableParameter('slider', "Number of Agents", 50, 10, 100, 1,
                               description="Choose how many agents to include in the model"),
        "token_supply": UserSettableParameter('slider', "Number of tokens", 5000, 1000, 10000, 1,
                                   description="Choose how many tokens in supply, tokens are split evenly among jurors at initialization."),
        "ratio": UserSettableParameter('slider', "Bonding Curve Reserve Ratio", 0.33, 0.01, 1, 0.01,
                                   description="Constant reserve ration maintained by the bonding curve different values change price function"),
        "agent_belief_sigma": UserSettableParameter('slider', "Agent Belief Sigma", 0.25, 0.05, 0.5, 0.05,
                                    description="standard deviation of agent beliefs, higher value means agents are more likely to make large trades"),
        "agent_starting_currency": UserSettableParameter('slider', "Agent Starting Currency", 100, 1, 1000, 1,
                                    description="standard deviation for agent beliefs of the true value relative to current price")

    })
server.port = 8521
server.launch()
