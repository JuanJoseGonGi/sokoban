from mesa import Agent
from mesa.space import Coordinate

from src.ai.a_star import a_star

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
            return

        _, path = a_star(
            self.pos,
            self.destination,
            self.model.heuristic_function(),
            ROBOT_ORDER,
            self.model.get_valid_move_neighbors,
        )

        next_position = None
        while len(path) > 0 and (self.pos == next_position or next_position is None):
            next_position = path.pop(0)

        if next_position is not None and next_position != self.pos:
            self.model.move_robot(self, next_position)

    def is_valid_move(self, next_position):
        return self.model.is_valid_robot_position(next_position)

    def find_box(self, box, pos):
        self.requester_box = box
        self.destination = pos

    def stop_finding(self):
        self.requester_box = None
        self.destination = None
