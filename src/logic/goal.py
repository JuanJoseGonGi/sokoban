from mesa import Agent
from mesa.space import Coordinate

from typing import Optional


class Goal(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.model = model
        self.pos: Optional[Coordinate] = None

    def step(self):
        pass
