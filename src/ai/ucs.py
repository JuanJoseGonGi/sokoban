import heapq


def ucs(model, origin, destination):
    def reconstruct_path(came_from, current):
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.append(current)
        return total_path[::-1]

    open_set = []
    heapq.heappush(open_set, (0, origin))

    came_from = {}
    cost_so_far = {origin: 0}
    visited = []  # Lista para almacenar los nodos visitados en orden

    while open_set:
        current_cost, current = heapq.heappop(open_set)
        visited.append(current)

        if current == destination:
            path = reconstruct_path(came_from, current)
            return visited, path  # Retorna las posiciones visitadas y la ruta

        for neighbor in model.get_valid_move_neighbors(current):
            new_cost = cost_so_far[current] + 1  # asumimos costo = 1 para cada paso
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost
                heapq.heappush(open_set, (priority, neighbor))
                came_from[neighbor] = current

    return visited, []
