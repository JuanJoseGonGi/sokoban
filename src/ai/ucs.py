import heapq

from typing import Callable


def ucs(
    origin,
    destination,
    order: tuple[str, str, str, str],
    is_valid_move_fn: Callable[[tuple[int, int], tuple[str, str, str, str]], list],
):
    def reconstruct_path(came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path[::-1]

    open_set = []
    heapq.heappush(open_set, (0, origin))

    came_from = {}
    cost_so_far = {origin: 0}
    visited = []  # Lista para mantener los nodos visitados en orden

    while open_set:
        current_cost, current = heapq.heappop(open_set)
        if current == destination:
            return visited, reconstruct_path(came_from, current)

        if current not in visited:
            visited.append(current)

        for neighbor in is_valid_move_fn(current, order):
            new_cost = cost_so_far[current] + 1  # Asumiendo costo = 1 para cada paso
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                heapq.heappush(open_set, (new_cost, neighbor))
                came_from[neighbor] = current

    # Si el destino no se encuentra
    return visited, []
