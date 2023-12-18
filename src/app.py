import mesa
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import Choice
from os import path

from src.ui.visualization.portrayal_router import PortrayalRouter
from src.logic.sokoban import Sokoban
from src.data.map_loader import MapLoader

loader = MapLoader()
map_structure, width, height = loader.get_map_structure(
    path.join(path.dirname(__file__), "data/samples/map4.txt")
)

portrayal_router = PortrayalRouter(show_path=False)
grid = mesa.visualization.CanvasGrid(
    portrayal_router.get_portrayal, width, height, width * 50, height * 50
)
server = ModularServer(
    Sokoban,
    [grid],
    "Sokoban",
    {
        "map_loader": loader,
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
        "find_solution_on_init": True,
    },
)

if __name__ == "__main__":
    server.port = 8521
    server.launch()
