from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation

from src.logic.box import Box
from src.logic.goal import Goal
from src.logic.path import Path
from src.logic.robot import Robot
from src.logic.rock import Rock
from src.ui.visualization.portrayal_router import PortrayalRouter

from src.ai.dfs import dfs
from src.ai.bfs import bfs
from src.ai.ucs import ucs
from src.ai.beam_search import beam_search
from src.ai.a_star import a_star
from src.ai.hill_climb import hill_climb

import pickle


class Sokoban(Model):
    def __init__(
        self,
        map_structure: dict[str, list[tuple[str, tuple[int, int]]]],
        width: int,
        height: int,
        portrayal_router: PortrayalRouter,
        algorithm_name: str,
        heuristic_function_name: str,
        origin_0: int,
        origin_1: int,
        destination_0: int,
        destination_1: int,
    ):
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.map_structure = map_structure
        self.portrayal_router = portrayal_router
        self.algorithm_name = algorithm_name
        self.heuristic_function_name = heuristic_function_name
        self.origin = (origin_0, origin_1)
        self.destination = (destination_0, destination_1)
        self.running = True
        self.agents = []

        for box in self.map_structure["boxes"]:
            self.agents.append(Box(len(self.agents), self, box[0]))
            self.grid.place_agent(self.agents[-1], box[1])

        for goal in self.map_structure["goals"]:
            self.agents.append(Goal(len(self.agents), self))
            self.grid.place_agent(self.agents[-1], goal[1])

        for path in self.map_structure["paths"]:
            self.agents.append(Path(len(self.agents), self))
            self.grid.place_agent(self.agents[-1], path[1])

        for robot in self.map_structure["robots"]:
            self.agents.append(Robot(len(self.agents), self, robot[0]))
            self.grid.place_agent(self.agents[-1], robot[1])

        for rock in self.map_structure["rocks"]:
            self.agents.append(Rock(len(self.agents), self))
            self.grid.place_agent(self.agents[-1], rock[1])

        self.portrayal_router.search_path = self.search_path()

        for agent in self.agents:
            self.schedule.add(agent)

    def step(self):
        #pass
        self.schedule.step()

    def get_position_agents(self, position: tuple[int, int]):
        return self.grid.get_cell_list_contents([position])

    def is_valid_position(self, position: tuple[int, int]) -> bool:
        if (
            position[0] < 0
            or position[0] >= self.grid.width
            or position[1] < 0
            or position[1] >= self.grid.height
        ):
            return False

        agents = self.get_position_agents(position)
        for agent in agents:
            if isinstance(agent, Box) or isinstance(agent, Rock):
                return False

        return True

    def get_valid_move_neighbors(
        self, position: tuple[int, int]
    ) -> list[tuple[int, int]]:
        """It returns the neighbors of a position following the left -> up -> right -> down order."""
        neighbors = [
            (position[0] - 1, position[1]),
            (position[0], position[1] + 1),
            (position[0] + 1, position[1]),
            (position[0], position[1] - 1),
        ]
        valid_neighbors = []
        for neighbor in neighbors:
            if self.is_valid_position(neighbor):
                valid_neighbors.append(neighbor)
        return valid_neighbors

    def get_valid_move_neighbors_and_costs(self, position: tuple[int, int]):
        neighbors = self.get_valid_move_neighbors(position)
        costs = [1] * len(neighbors)
        return neighbors, costs

    def heuristic_function(self):
        if self.heuristic_function_name == "Manhattan Distance":
            return lambda position, destination: abs(
                position[0] - destination[0]
            ) + abs(position[1] - destination[1])
        if self.heuristic_function_name == "Euclidean Distance":
            return (
                lambda position, destination: (
                    (position[0] - destination[0]) ** 2
                    + (position[1] - destination[1]) ** 2
                )
                ** 0.5
            )

        raise NotImplementedError

    def search_path(self) -> list[tuple[int, int]]:
        if self.algorithm_name == "DFS":
            visited, _ = dfs(self, self.origin, self.destination)
            return visited
        if self.algorithm_name == "BFS":
            visited, _ = bfs(self, self.origin, self.destination)
            return visited
        if self.algorithm_name == "UCS":
            visited, _ = ucs(self, self.origin, self.destination)

            print(_)#la ruta

            #guardar la ruta de los nodos que debe visitar en orden
            with open('src/data/path.pkl', 'wb') as f:
                pickle.dump(_, f)

            return visited
        if self.algorithm_name == "Beam Search":
            visited, _ = beam_search(
                self, self.heuristic_function(), 2, self.origin, self.destination
            )
            return visited
        if self.algorithm_name == "A*":
            visited, _ = a_star(
                self, self.origin, self.destination, self.heuristic_function()
            )
            return visited
        if self.algorithm_name == "Hill Climbing":
            visited, _ = hill_climb(
                self, self.origin, self.destination, self.heuristic_function()
            )
            return visited

        raise NotImplementedError
