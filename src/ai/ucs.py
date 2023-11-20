from collections import deque


def ucs(model, origin, destination):
    def reconstruct_path(came_from, current):
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.append(current)
        return total_path[::-1]

    queue: deque[tuple[int, tuple[int, int]]] = deque([(0, origin)])

    came_from = {}
    cost_so_far = {origin: 0}
    visited = []  # Conjunto de nodos visitados
    explored = []  # Conjunto de nodos explorados

    while queue:
        current_cost, current = queue.pop()

        if current == destination:
            path = reconstruct_path(came_from, current)
            visited.append(current)
            return list(visited), path  # Retorna las posiciones visitadas y la ruta

        if current not in explored:
            explored.append(current)
            visited.append(current)

            for neighbor in model.get_valid_move_neighbors(current):
                new_cost = cost_so_far[current] + 1  # Asumimos costo = 1 para cada paso
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost
                    queue.appendleft((priority, neighbor))
                    came_from[neighbor] = current

    return list(visited), []
