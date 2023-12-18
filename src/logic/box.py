from mesa import Agent
from mesa.space import Coordinate

from src.logic.robot import Robot

from typing import Optional


class Box(Agent):
    def __init__(self, unique_id, model, name: str):
        super().__init__(unique_id, model)
        self.model = model
        self.name = name
        self.path = []
        self.requested_robot: Optional[Robot] = None
        self.pos: Optional[Coordinate] = None

    def step(self) -> None:
        if len(self.path) > 0:
            self.move()

        return None

    def move(self):
        if len(self.path) < 1:
            return

        next_position = self.path[0]

        if self.model.move_box(self, next_position):
            self.path.pop(0)

    def is_valid_move(self, next_position):
        return self.model.is_valid_box_position(next_position)
