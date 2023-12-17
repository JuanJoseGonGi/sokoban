from mesa import Agent
import pickle

class Robot(Agent):
    def __init__(self, unique_id, model, name: str):
        super().__init__(unique_id, model)
        self.name = name

        self.counter = 0
        self.route = self.path_robot(self.routes())

    def step(self):
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

    def path_robot(self,routeBox):
        path = []
        for i in range(len(routeBox)):
            if i+1 == len(routeBox):
                break
            path.append(self.determine_movement(routeBox[i],routeBox[i+1]))
        return path

    #given the x,y of 2 coordinates of the box, it returns the position of the robot
    #coord1 tuple[int, int], coord2 tuple[int, int]
    def determine_movement(self,coord1, coord2):

        if(coord2[0]>coord1[0] and coord2[1] == coord1[1]):#derecha
            return coord1
        elif(coord2[0]<coord1[0] and coord2[1] == coord1[1]):#izquierda
            return coord2
        elif(coord2[0] == coord1[0] and coord2[1] > coord1[1]):#arriba
            return coord1
        elif(coord2[0] == coord1[0] and coord2[1] < coord1[1]):#abajo
            return coord2
