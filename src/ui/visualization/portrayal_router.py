from os import path

from mesa import Agent

from src.logic.box import Box
from src.logic.goal import Goal
from src.logic.path import Path
from src.logic.robot import Robot
from src.logic.rock import Rock


def get_box_portrayal():
    return {
        "Shape": path.join(path.dirname(__file__), "images/package.png"),
        "Layer": 1,
    }


def get_goal_portrayal():
    return {
        "Shape": path.join(path.dirname(__file__), "images/flag.png"),
        "Layer": 1,
    }


def get_path_portrayal():
    return {
        "Shape": path.join(path.dirname(__file__), "images/floor.png"),
        "Layer": 0,
    }


def get_robot_portrayal():
    return {
        "Shape": path.join(path.dirname(__file__), "images/robot.png"),
        "Layer": 2,
    }


def get_rock_portrayal():
    return {
        "Shape": path.join(path.dirname(__file__), "images/wall.png"),
        "Layer": 2,
    }


class PortrayalRouter:
    def get_portrayal(self, agent: Agent):
        if isinstance(agent, Box):
            return get_box_portrayal()
        if isinstance(agent, Goal):
            return get_goal_portrayal()
        if isinstance(agent, Path):
            return get_path_portrayal()
        if isinstance(agent, Robot):
            return get_robot_portrayal()
        if isinstance(agent, Rock):
            return get_rock_portrayal()

        raise NotImplementedError
