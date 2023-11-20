from src.logic.sokoban import Sokoban
from collections import deque


def bfs(model: Sokoban, origin: tuple[int, int], destination: tuple[int, int]):
    """Recursive implementation of BFS.

    It receives a model, an origin, and a destination, and returns a list
    of visited positions and a set of positions that form a path from the
    origin to the destination.
    """
    visited_positions = []
    path = set()

    def bfs_recursive(
        origin: tuple[int, int],
        queue: deque[tuple[int, int]],
    ):
        visited_positions.append(origin)
        if origin == destination:
            path.add(origin)
            return True
        for neighbor in model.get_valid_move_neighbors(origin):
            if neighbor not in visited_positions:
                queue.append(neighbor)
        if len(queue) > 0:
            return bfs_recursive(queue.popleft(), queue)
        return False

    bfs_recursive(origin, deque())
    return visited_positions, path
