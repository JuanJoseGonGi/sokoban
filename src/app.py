from mesa.visualization.ModularVisualization import ModularServer
import mesa
from os import path

from src.ui.visualization.portrayal_router import PortrayalRouter
from src.logic.sokoban import Sokoban
from src.data.map_loader import MapLoader

loader = MapLoader()
map_structure, width, height = loader.get_map_structure(
    path.join(path.dirname(__file__), "data/samples/map1.txt")
)

portrayal_router = PortrayalRouter()
grid = mesa.visualization.CanvasGrid(
    portrayal_router.get_portrayal, width, height, width * 50, height * 50
)
server = ModularServer(
    Sokoban,
    [grid],
    "Sokoban",
    {"map_structure": map_structure, "width": width, "height": height},
)

if __name__ == "__main__":
    server.port = 8521
    server.launch()
