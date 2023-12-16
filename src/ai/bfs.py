from collections import deque

from typing import Union


def bfs(model, origin: tuple[int, int], destination: tuple[int, int]):
    """Iterative implementation of BFS.

    It receives a model, an origin, and a destination, and returns a list
    of visited positions and a list that forms a path from the
    origin to the destination.
    """
    visited_positions = []
    queue = deque([origin])
    came_from: dict[tuple[int, int], Union[tuple[int, int], None]] = {origin: None}

    while queue:
        current = queue.popleft()
        visited_positions.append(current)

        if current == destination:
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            return list(visited_positions), path[::-1]

        for neighbor in model.get_valid_move_neighbors(current):
            if neighbor not in visited_positions and neighbor not in queue:
                queue.append(neighbor)
                came_from[neighbor] = current

    return visited_positions, []
