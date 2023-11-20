from mesa import Agent


class Box(Agent):
    def __init__(self, unique_id, model, name: str):
        super().__init__(unique_id, model)
        self.name = name

    def step(self):
        pass
