import mesa
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Choice, NumberInput
from os import path

from src.ui.visualization.portrayal_router import PortrayalRouter
from src.logic.sokoban import Sokoban
from src.data.map_loader import MapLoader

loader = MapLoader()
map_structure, width, height = loader.get_map_structure(
    path.join(path.dirname(__file__), "data/samples/map2.txt")
)

portrayal_router = PortrayalRouter()
grid = mesa.visualization.CanvasGrid(
    portrayal_router.get_portrayal, width, height, width * 50, height * 50
)
server = ModularServer(
    Sokoban,
    [grid],
    "Sokoban",
    {
        "map_structure": map_structure,
        "width": width,
        "height": height,
        "portrayal_router": portrayal_router,
        "algorithm_name": Choice(
            "Algorithm",
            "DFS",
            ["DFS", "BFS", "UCS", "Beam Search", "A*", "Hill Climbing"],
        ),
        "heuristic_function_name": Choice(
            "Heuristic Function",
            "Manhattan Distance",
            ["Manhattan Distance", "Euclidean Distance"],
        ),
        "origin_0": NumberInput("Origin X", 0),
        "origin_1": NumberInput("Origin Y", 4),
        "destination_0": NumberInput("Destination X", 6),
        "destination_1": NumberInput("Destination Y", 2),
    },
)

if __name__ == "__main__":
    server.port = 8521
    server.launch()
