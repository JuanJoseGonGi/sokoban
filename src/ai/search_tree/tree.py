from os import path
import heapq
from collections import deque
from typing import Union

from src.logic.box import Box
from src.logic.robot import Robot
from src.logic.rock import Rock
from src.logic.goal import Goal
from src.logic.path import Path

Agent = Union[Robot, Box, Rock, Goal, Path]


class TreeNode:
    def __init__(self, model, parent=None, cost=0, box_move=None):
        self.model = model
        self.parent = parent
        self.children = []
        self.cost = cost  # Costo acumulado
        self.box_move = box_move

    def add_child(self, child):
        self.children.append(child)

    def is_final_state(self):
        return not self.model.has_unsolved_goals()

    def expand(self, order: tuple[str, str, str, str], visited: set):
        boxes = self.model.get_boxes()
        for box in boxes:
            if box.pos is None:
                continue

            neighbors = self.model.get_valid_box_move_neighbors(box.pos, order)
            for neighbor in neighbors:
                new_model = self.model.copy()
                new_model_box = new_model.get_box(box.name)
                new_model.move_agent(new_model_box, neighbor, teleport_box_robot=True)

                if new_model in visited:
                    continue

                box_move = (box.name, box.pos, neighbor)
                new_node = TreeNode(new_model, self, self.cost + 1, box_move)
                self.add_child(new_node)

        return self.children

    def __lt__(self, other):
        return self.cost < other.cost


class Tree:
    def __init__(self, model, order: tuple[str, str, str, str]):
        self.root = TreeNode(model)
        self.order = order
        self.visited = set()

    def nodes(self):
        nodes = []
        self._nodes(self.root, nodes)
        return nodes

    def _nodes(self, node: TreeNode, nodes: list):
        nodes.append(node)
        for child in node.children:
            self._nodes(child, nodes)

    def save_to_files(self, dir_path: str):
        nodes = self.nodes()
        print(f"Saving {len(nodes)} nodes to {dir_path}")
        node_count = 0
        for node in nodes:
            file_path = path.join(dir_path, f"{node_count}.txt")
            if not node.model.has_unsolved_goals():
                file_path = path.join(dir_path, f"{node_count}_final.txt")

            node.model.save_current_structure(file_path)
            node_count += 1

    def expand_node(self, node, queue, visited, is_beam_search=False, beam_width=None):
        node.expand(self.order, visited)
        for child in node.children:
            total_cost = child.cost + child.model.get_cost()
            heapq.heappush(queue, (total_cost, str(child.model), child))

        if is_beam_search and beam_width is not None:
            queue = heapq.nsmallest(beam_width, queue)

    def bfs(self):
        queue = deque([self.root])
        while queue:
            node = queue.popleft()
            if node.model in self.visited:
                continue

            self.visited.add(node.model)

            if node.is_final_state():
                return node

            node.expand(self.order, self.visited)
            for child in node.children:
                queue.append(child)

        return None

    def dfs(self):
        stack = [self.root]
        while stack:
            node = stack.pop()
            if node.model in self.visited:
                continue

            self.visited.add(node.model)

            if node.is_final_state():
                return node

            node.expand(self.order, self.visited)
            for child in node.children:
                stack.append(child)

        return None

    def ucs(self):
        # Usar una cola de prioridad para gestionar los nodos por costo
        queue = [(self.root.cost, self.root)]
        while queue:
            cost, node = heapq.heappop(queue)
            if node.model in self.visited:
                continue

            self.visited.add(node.model)

            if node.is_final_state():
                return node

            node.expand(self.order, self.visited)
            for child in node.children:
                heapq.heappush(queue, (child.cost, child))

        return None

    def a_star(self):
        queue = []
        start_cost = self.root.cost + self.root.model.get_cost()
        heapq.heappush(queue, (start_cost, str(self.root.model), self.root))

        while queue:
            _, _, node = heapq.heappop(queue)
            if node.model in self.visited:
                continue

            self.visited.add(node.model)

            if node.is_final_state():
                return node

            self.expand_node(node, queue, self.visited)

        return None

    def beam_search(self, beam_width: int):
        queue = [
            (
                self.root.cost + self.root.model.get_cost(),
                str(self.root.model),
                self.root,
            )
        ]

        while queue:
            _, _, node = heapq.heappop(queue)
            if node.model in self.visited:
                continue

            self.visited.add(node.model)

            if node.is_final_state():
                return node

            self.expand_node(
                node, queue, self.visited, is_beam_search=True, beam_width=beam_width
            )

        return None

    def hill_climbing(self):
        current_node = self.root
        self.visited.add(current_node.model)

        while True:
            if current_node.is_final_state():
                return current_node

            children = current_node.expand(self.order, self.visited)
            if not children:
                break  # No more moves available

            current_node = max(children, key=lambda child: -child.model.get_cost())
            if current_node.model in self.visited:
                break  # No better move found

            self.visited.add(current_node.model)

        return None
