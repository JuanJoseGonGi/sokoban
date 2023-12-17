from mesa import Agent
import pickle

class Box(Agent):
    def __init__(self, unique_id, model, name: str):
        super().__init__(unique_id, model)
        self.name = name
        self.counter = 1
        self.route = self.routes()

    def step(self):
        try:
            position_xy = self.route[self.counter]
            self.model.grid.move_agent(self,position_xy )
            #print("stepbox",)
            self.counter += 1
        except:
            print("no more steps, the goal was reached or all the route was traversed")

    def routes(self):
        with open('src/data/path.pkl', 'rb') as f:
            return pickle.load(f)
