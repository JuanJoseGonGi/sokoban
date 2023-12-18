from collections import deque
from typing import Union, Callable


def bfs(
    origin: tuple[int, int],
    destination: tuple[int, int],
    order: tuple[str, str, str, str],
    is_valid_move_fn: Callable[[tuple[int, int], tuple[str, str, str, str]], list],
):
    visited_positions = [origin]
    queue = deque([origin])
    came_from: dict[tuple[int, int], Union[tuple[int, int], None]] = {origin: None}
    path = []

    while queue:
        current = queue.popleft()
        if current == destination:
            while current:
                path.append(current)
                current = came_from[current]
            return visited_positions, path[::-1]

        for neighbor in is_valid_move_fn(current, order):
            if neighbor not in visited_positions:
                queue.append(neighbor)
                visited_positions.append(neighbor)
                came_from[neighbor] = current

    return visited_positions, path
