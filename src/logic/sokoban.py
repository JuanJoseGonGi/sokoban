from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation

from src.logic.box import Box
from src.logic.goal import Goal
from src.logic.path import Path
from src.logic.robot import Robot
from src.logic.rock import Rock


class Sokoban(Model):
    def __init__(
        self, map_structure: dict[str, list[tuple[str, tuple[int, int]]]], width, height
    ):
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.map_structure = map_structure
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

        # for agent in self.agents:
        #     self.schedule.add(agent)

    def step(self):
        pass
        # self.schedule.step()

    def get_position_agents(self, position: tuple[int, int]):
        return self.grid.get_cell_list_contents([position])

    def is_valid_position(self, position: tuple[int, int]) -> bool:
        if position[0] < 0 or position[0] >= self.grid.width:
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
            (position[0], position[1] - 1),
            (position[0] + 1, position[1]),
            (position[0], position[1] + 1),
        ]
        valid_neighbors = []
        for neighbor in neighbors:
            if self.is_valid_position(neighbor):
                valid_neighbors.append(neighbor)
        return valid_neighbors
