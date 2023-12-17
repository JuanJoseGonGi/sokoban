from mesa import Agent
import pickle

class Robot(Agent):
    def __init__(self, unique_id, model, name: str):
        super().__init__(unique_id, model)
        self.name = name

        self.counter = 0
        # self.route = self.path_robot(self.routes())
        self.route = self.routes()

    def step(self):
        if self.counter == len(self.route)-1:
            print("no more steps, the goal was reached or all the route was traversed")
            return
        try:
            position_xy = self.route[self.counter]
            self.model.grid.move_agent(self,position_xy )
            print("steprobot",self.route)
            self.counter += 1
        except:
            print("no more steps, the goal was reached or all the route was traversed")

    def routes(self):
        #the path of the box
        with open('src/data/path.pkl', 'rb') as f:
            return pickle.load(f)
