from mesa import Model
from mesa.space import MultiGrid, Coordinate
from mesa.time import RandomActivation

from src.logic.box import Box
from src.logic.goal import Goal
from src.logic.path import Path
from src.logic.robot import Robot
from src.logic.rock import Rock
from src.ui.visualization.portrayal_router import PortrayalRouter

from src.ai.dfs import dfs
from src.ai.bfs import bfs
from src.ai.ucs import ucs
from src.ai.beam_search import beam_search
from src.ai.a_star import a_star
from src.ai.hill_climb import hill_climb
from src.ai.search_tree.tree import Tree, TreeNode

from src.data.map_loader import MapLoader

import os
from typing import Callable, Union, Optional

ROBOT_ORDER = ("left", "up", "right", "down")
BOX_ORDER = ("down", "up", "left", "right")


class Sokoban(Model):
    def __init__(
        self,
        map_loader: MapLoader,
        map_structure: dict[str, list[tuple[str, Coordinate]]],
        width: int,
        height: int,
        portrayal_router: PortrayalRouter,
        algorithm_name: str,
        heuristic_function_name: str,
        find_solution_on_init=False,
    ):
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.map_loader = map_loader
        self.map_structure = map_structure
        self.portrayal_router = portrayal_router
        self.algorithm_name = algorithm_name
        self.heuristic_function_name = heuristic_function_name
        self.agents = []

        for box in self.map_structure["boxes"]:
            self.agents.append(Box(len(self.agents), self, box[0]))
            self.grid.place_agent(self.agents[-1], box[1])

        for goal in self.map_structure["goals"]:
            self.agents.append(Goal(len(self.agents), self))
            self.grid.place_agent(self.agents[-1], goal[1])

        for path in self.map_structure["paths"]:
            self.agents.append(Path(len(self.agents), self))
            self.grid.place_agent(self.agents[-1], path[1])

        for robot in self.map_structure["robots"]:
            self.agents.append(Robot(len(self.agents), self, robot[0]))
            self.grid.place_agent(self.agents[-1], robot[1])

        for rock in self.map_structure["rocks"]:
            self.agents.append(Rock(len(self.agents), self))
            self.grid.place_agent(self.agents[-1], rock[1])

        for agent in self.agents:
            self.schedule.add(agent)

        if find_solution_on_init:
            self.find_solution()

    def step(self):
        if not self.has_unsolved_goals():
            self.running = False
            return

        self.schedule.step()

    def get_position_agents(self, position: Coordinate):
        return self.grid.get_cell_list_contents([position])

    def is_valid_robot_position(self, position: Coordinate) -> bool:
        if (
            position[0] < 0
            or position[0] >= self.grid.width
            or position[1] < 0
            or position[1] >= self.grid.height
        ):
            return False

        agents = self.get_position_agents(position)
        for agent in agents:
            if isinstance(agent, Box) or isinstance(agent, Rock):
                return False

        return True

    def get_reachable_robots_sorted_by_distance(
        self, position: Coordinate
    ) -> list[Robot]:
        if not self.is_valid_robot_position(position):
            return []

        robots = self.get_robots(
            key=lambda robot: self.heuristic_function()(position, robot.pos)
        )
        reachable_robots = []
        for robot in robots:
            if robot.pos is None:
                continue

            _, path = self.get_path(
                robot.pos, position, ROBOT_ORDER, self.get_valid_move_neighbors
            )
            if len(path) == 0:
                continue

            reachable_robots.append(robot)

        return reachable_robots

    def is_robot_reachable_position(self, position: Coordinate) -> bool:
        return len(self.get_reachable_robots_sorted_by_distance(position)) > 0

    def get_direction_move(self, direction: str) -> Coordinate:
        if direction == "up":
            return (0, 1)
        if direction == "right":
            return (1, 0)
        if direction == "down":
            return (0, -1)
        if direction == "left":
            return (-1, 0)

        raise Exception(f"Unknown direction: {direction}")

    def get_valid_move_neighbors(
        self, position: Coordinate, order: tuple[str, str, str, str]
    ) -> list[Coordinate]:
        """It returns the neighbors of a position following the given order."""

        neighbors = []

        for i in range(4):
            neighbors.append(
                (
                    position[0] + self.get_direction_move(order[i])[0],
                    position[1] + self.get_direction_move(order[i])[1],
                )
            )

        valid_neighbors = []
        for neighbor in neighbors:
            if self.is_valid_robot_position(neighbor):
                valid_neighbors.append(neighbor)

        return valid_neighbors

    def get_opposite_position(self, current: Coordinate, new: Coordinate) -> Coordinate:
        if current[0] - 1 == new[0]:
            return (current[0] + 1, current[1])
        if current[0] + 1 == new[0]:
            return (current[0] - 1, current[1])
        if current[1] - 1 == new[1]:
            return (current[0], current[1] + 1)
        if current[1] + 1 == new[1]:
            return (current[0], current[1] - 1)

        raise Exception(f"Unknown direction: {current} -> {new}")

    def is_valid_box_position(self, position: Coordinate) -> bool:
        if not self.is_valid_robot_position(position):
            return False

        if self.has_robot_at(position):
            return False

        return True

    def is_valid_box_move(self, position: Coordinate, new_position: Coordinate) -> bool:
        if position == new_position:
            return True

        opposite = self.get_opposite_position(position, new_position)
        return self.is_valid_box_position(
            new_position
        ) and self.is_robot_reachable_position(opposite)

    def get_valid_box_move_neighbors(
        self, position: Coordinate, order: tuple[str, str, str, str]
    ):
        neighbors = self.get_valid_move_neighbors(position, order)

        valid_neighbors = []
        for neighbor in neighbors:
            if self.is_valid_box_move(position, neighbor):
                valid_neighbors.append(neighbor)

        return valid_neighbors

    def heuristic_function(self):
        if self.heuristic_function_name == "Manhattan Distance":
            return lambda position, destination: abs(
                position[0] - destination[0]
            ) + abs(position[1] - destination[1])
        if self.heuristic_function_name == "Euclidean Distance":
            return (
                lambda position, destination: (
                    (position[0] - destination[0]) ** 2
                    + (position[1] - destination[1]) ** 2
                )
                ** 0.5
            )

        raise NotImplementedError

    def get_path(
        self,
        origin: Coordinate,
        destination: Coordinate,
        order: tuple[str, str, str, str],
        is_valid_move_fn: Callable[[Coordinate, tuple[str, str, str, str]], list],
    ) -> tuple[list[Coordinate], list[Coordinate]]:
        if self.algorithm_name == "DFS":
            visited, path = dfs(origin, destination, order, is_valid_move_fn)
            return visited, path
        if self.algorithm_name == "BFS":
            visited, path = bfs(origin, destination, order, is_valid_move_fn)
            return visited, path
        if self.algorithm_name == "UCS":
            visited, path = ucs(origin, destination, order, is_valid_move_fn)
            return visited, path
        if self.algorithm_name == "Beam Search":
            visited, path = beam_search(
                self.heuristic_function(),
                2,
                origin,
                destination,
                order,
                is_valid_move_fn,
            )
            return visited, path
        if self.algorithm_name == "A*":
            visited, path = a_star(
                origin, destination, self.heuristic_function(), order, is_valid_move_fn
            )
            return visited, path
        if self.algorithm_name == "Hill Climbing":
            visited, path = hill_climb(
                origin, destination, self.heuristic_function(), order, is_valid_move_fn
            )
            return visited, path

        raise NotImplementedError

    def move_agent(
        self, agent: Union[Robot, Box], position: Coordinate, teleport_box_robot=False
    ) -> bool:
        if agent.pos == position:
            return True

        if isinstance(agent, Robot) and not self.is_valid_robot_position(position):
            return False

        if isinstance(agent, Robot):
            self.grid.move_agent(agent, position)
            return True

        if agent.pos is None:
            raise Exception(f"Agent {agent.name} position is None")

        if not self.is_valid_box_move(agent.pos, position):
            return False

        opposite = self.get_opposite_position(agent.pos, position)
        if agent.requested_robot is not None and agent.requested_robot.pos == opposite:
            self.grid.move_agent(agent.requested_robot, agent.pos)
            self.grid.move_agent(agent, position)
            agent.requested_robot = None
            return True

        if agent.requested_robot is not None:
            if not teleport_box_robot:
                print(
                    f"Waiting for robot {agent.requested_robot.name} to move to {opposite}"
                )
                print(f"Current position: {agent.requested_robot.pos}")
                return False  # wait for the robot to move

            self.grid.move_agent(agent, position)
            return True

        robots = self.get_reachable_robots_sorted_by_distance(opposite)
        for robot in robots:
            if robot.pos is None:
                continue

            if robot.destination is not None:
                continue

            if teleport_box_robot:
                self.grid.move_agent(agent, position)
                return True

            robot.destination = opposite
            robot.requester_box = agent
            agent.requested_robot = robot

            return False

        return False

    def has_robot_at(self, position: Coordinate) -> bool:
        agents = self.get_position_agents(position)
        for agent in agents:
            if isinstance(agent, Robot):
                return True

        return False

    def get_goals(self) -> set[Goal]:
        goals = set()
        for agent in self.agents:
            if isinstance(agent, Goal):
                goals.add(agent)

        return goals

    def get_unsolved_goals(self) -> set[Goal]:
        all_goals = self.get_goals()
        solved_goals = set()

        for goal in all_goals:
            if goal.pos is None:
                continue

            agents = self.get_position_agents(goal.pos)
            for agent in agents:
                if isinstance(agent, Box):
                    solved_goals.add(goal)
                    break

        return all_goals - solved_goals

    def has_unsolved_goals(self) -> bool:
        return len(self.get_unsolved_goals()) > 0

    def get_robots(self, key=None) -> list[Robot]:
        robots = []
        for agent in self.agents:
            if isinstance(agent, Robot):
                robots.append(agent)

        if key is not None:
            robots.sort(key=key)

        return robots

    def get_boxes(self) -> list[Box]:
        boxes = []
        for agent in self.agents:
            if isinstance(agent, Box):
                boxes.append(agent)

        boxes.sort(key=lambda box: box.pos[0])
        return boxes

    def get_box(self, name: str) -> Box:
        for agent in self.agents:
            if isinstance(agent, Box) and agent.name == name:
                return agent

        raise Exception(f"Box {name} not found")

    def build_search_tree(self) -> tuple[Tree, Optional[TreeNode]]:
        tree = Tree(self, BOX_ORDER)
        solution_node = None

        if self.algorithm_name == "DFS":
            solution_node = tree.dfs()
        elif self.algorithm_name == "BFS":
            solution_node = tree.bfs()
        elif self.algorithm_name == "UCS":
            solution_node = tree.ucs()
        elif self.algorithm_name == "Beam Search":
            solution_node = tree.beam_search(3)
        elif self.algorithm_name == "A*":
            solution_node = tree.a_star()
        elif self.algorithm_name == "Hill Climbing":
            solution_node = tree.hill_climbing()

        return tree, solution_node

    def find_solution(self) -> None:
        tree, solution_node = self.build_search_tree()
        tree.save_to_files(os.path.join("data", "search_tree", self.algorithm_name))
        if solution_node is None:
            return

        # Asignar los caminos reconstruidos a las cajas
        box_paths = self.reconstruct_box_paths(solution_node)
        for box_name, path in box_paths.items():
            box = self.get_box(box_name)
            box.path = [
                move[1] for move in path
            ]  # Solo necesitamos las posiciones finales

    def reconstruct_box_paths(
        self, solution_node: TreeNode
    ) -> dict[str, list[tuple[Coordinate, Coordinate]]]:
        current_node = solution_node
        box_paths: dict[str, list[tuple[Coordinate, Coordinate]]] = {}

        while current_node.parent is not None:
            if current_node.box_move:
                box_name, start_pos, end_pos = current_node.box_move
                if box_name not in box_paths:
                    box_paths[box_name] = []
                box_paths[box_name].insert(0, (start_pos, end_pos))
            current_node = current_node.parent

        return box_paths

    def get_current_map_structure(self):
        map_structure: dict[str, list[tuple[str, Coordinate]]] = {
            "paths": [],
            "rocks": [],
            "goals": [],
            "robots": [],
            "boxes": [],
        }

        for agent in self.agents:
            if agent.pos is None:
                continue

            if isinstance(agent, Goal):
                map_structure["goals"].append(("M", agent.pos))
                continue

            if isinstance(agent, Path):
                map_structure["paths"].append(("C", agent.pos))
                continue

            if isinstance(agent, Rock):
                map_structure["rocks"].append(("R", agent.pos))
                continue

            if isinstance(agent, Robot):
                map_structure["robots"].append((agent.name, agent.pos))
                continue

            if isinstance(agent, Box):
                map_structure["boxes"].append((agent.name, agent.pos))
                continue

        return map_structure

    def save_current_structure(self, path: str):
        self.map_loader.save_map_to_file(self.get_current_map_structure(), path)

    def __str__(self):
        return "".join(
            self.map_loader.map_structure_to_strings(self.get_current_map_structure())
        )

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.get_current_map_structure() == other.get_current_map_structure()

    def __hash__(self):
        return hash(str(self))

    def copy(self):
        return Sokoban(
            self.map_loader,
            self.get_current_map_structure(),
            self.grid.width,
            self.grid.height,
            self.portrayal_router,
            self.algorithm_name,
            self.heuristic_function_name,
        )

    def get_cost(self) -> int:
        total_cost = 0

        for box in self.get_boxes():
            if box.pos is None:
                continue

            box_cost = 100000000

            for goal in self.get_goals():
                if goal.pos is None:
                    continue

                box_cost = min(box_cost, self.heuristic_function()(box.pos, goal.pos))

            total_cost += box_cost

        robots = self.get_robots()
        for robot in robots:
            if robot.pos is None:
                continue

            robot_cost = 100000000

            for goal in self.get_goals():
                if goal.pos is None:
                    continue

                robot_cost = min(
                    robot_cost, self.heuristic_function()(robot.pos, goal.pos)
                )

            total_cost += robot_cost

        return total_cost
