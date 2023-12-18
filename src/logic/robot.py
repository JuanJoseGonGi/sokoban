from mesa import Agent
from mesa.space import Coordinate

from typing import Optional

ROBOT_ORDER = ("left", "up", "right", "down")


class Robot(Agent):
    def __init__(self, unique_id, model, name: str):
        super().__init__(unique_id, model)
        self.model = model
        self.name = name
        self.destination: Optional[Coordinate] = None
        self.pos: Optional[Coordinate] = None
        self.requester_box: Optional[Agent] = None

    def step(self):
        self.move()

    def move(self):
        if self.destination is None:
            return

        if self.pos == self.destination:
            self.destination = None
            self.requester_box = None
            return

        _, path = self.model.get_path(
            self.pos,
            self.destination,
            ROBOT_ORDER,
            self.model.get_valid_move_neighbors,
        )

        next_position = path.pop(0)
        while len(path) > 0 and self.pos == next_position:
            next_position = path.pop(0)

        if next_position != self.pos:
            self.model.move_agent(self, next_position)
            return

        self.destination = None
        self.requester_box = None

    def is_valid_move(self, next_position):
        return self.model.is_valid_robot_position(next_position)
