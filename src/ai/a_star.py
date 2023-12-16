import heapq


def a_star(model, origin, destination, heuristic):
    def reconstruct_path(came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path[::-1]

    open_set = []
    heapq.heappush(open_set, (0, origin))
    open_set_hash = {origin}  # Conjunto para rastrear los elementos en open_set

    came_from = {}
    g_score = {origin: 0}
    f_score = {origin: heuristic(origin, destination)}
    visited = []  # Lista para almacenar los nodos visitados en orden

    while open_set:
        current = heapq.heappop(open_set)[1]
        open_set_hash.remove(current)
        visited.append(current)  # Añadir el nodo actual a la lista de visitados

        if current == destination:
            return visited, reconstruct_path(came_from, current)

        for neighbor in model.get_valid_move_neighbors(current):
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, destination)
                if neighbor not in open_set_hash:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    open_set_hash.add(neighbor)

    return visited, []
