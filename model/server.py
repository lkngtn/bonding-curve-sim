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
    canvas_height=150, canvas_width=150
)

chart2 = ChartModule([
    {"Label": "Price", "Color": "#56bfdf"}],
    data_collector_name='datacollector',
    canvas_height=150, canvas_width=150
)

chart3 = ChartModule([
    {"Label": "Token_Supply", "Color": "#56bfdf"},
    {"Label": "Currency_Supply", "Color": "#c66657"}],
    data_collector_name='datacollector',
    canvas_height=300, canvas_width=300
)

chart4 = ChartModule([{"Label": "Total_Wealth", "Color": "#7bb36e"}],
    data_collector_name='datacollector',
    canvas_height=300, canvas_width=300
)


server = ModularServer(
    RandomMarket,
    [chart3,chart4,chart1,chart2],
    name="Random Agent Bonding Curve Sim",
    model_params={
        "ratio": UserSettableParameter('slider', "Bonding Curve Reserve Ratio", 0.33, 0.01, 1.0, 0.01,
                                       description="Constant reserve ration maintained by the bonding curve different values change price function"),
        "num_agents": UserSettableParameter('slider', "Number of Agents", 50, 10, 100, 1,
                               description="Choose how many agents to include in the model"),
        "token_supply": UserSettableParameter('slider', "Number of tokens", 5000, 1000, 10000, 1,
                                   description="Choose how many tokens in supply, tokens are split evenly among jurors at initialization."),
        "agent_starting_currency": UserSettableParameter('slider', "Agent Starting Currency", 100, 1, 1000, 1,
                                    description="standard deviation for agent beliefs of the true value relative to current price")

    })
server.port = 8521
server.launch()
