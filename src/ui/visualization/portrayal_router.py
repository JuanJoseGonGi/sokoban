from os import path

from mesa import Agent

from src.logic.box import Box
from src.logic.goal import Goal
from src.logic.path import Path
from src.logic.robot import Robot
from src.logic.rock import Rock


class PortrayalRouter:
    def __init__(
        self, search_path: list[tuple[int, int]] = [], show_path: bool = False
    ):
        self.search_path = search_path
        self.show_path = show_path

    def get_portrayal(self, agent: Agent):
        text = ""
        if self.show_path and agent.pos in self.search_path:
            text = self.search_path.index(agent.pos)

        portrayal = {"text": text, "text_color": "#000000", "Color": "#000000"}

        if isinstance(agent, Box):
            portrayal.update(self.get_box_portrayal(agent))
            return portrayal
        elif isinstance(agent, Goal):
            portrayal.update(self.get_goal_portrayal(agent))
            return portrayal
        if isinstance(agent, Path):
            portrayal.update(self.get_path_portrayal(agent))
            return portrayal
        if isinstance(agent, Robot):
            portrayal.update(self.get_robot_portrayal(agent))
            return portrayal
        if isinstance(agent, Rock):
            portrayal.update(self.get_rock_portrayal(agent))
            return portrayal

        raise NotImplementedError

    def get_box_portrayal(self, box: Box):
        return {
            "Shape": path.join(path.dirname(__file__), "images/package.png"),
            "Layer": 2,
        }

    def get_goal_portrayal(self, goal: Goal):
        return {
            "Shape": path.join(path.dirname(__file__), "images/flag.png"),
            "Layer": 0,
        }

    def get_path_portrayal(self, sokoban_path: Path):
        # return {
        #     "Shape": path.join(path.dirname(__file__), "images/floor.png"),
        #     "Layer": 0,
        # }

        return {
            "Shape": "rect",
            "Filled": "true",
            "Layer": 0,
            "w": 1,
            "h": 1,
            "Color": "#FFFFFF",
        }

    def get_robot_portrayal(self, robot: Robot):
        return {
            "Shape": path.join(path.dirname(__file__), "images/robot.png"),
            "Layer": 1,
            "text": robot.name,
            "text_color": "#FFFFFF",
            "Color": "#FFFFFF",
        }

    def get_rock_portrayal(self, rock: Rock):
        return {
            "Shape": path.join(path.dirname(__file__), "images/wall.png"),
            "Layer": 1,
        }
