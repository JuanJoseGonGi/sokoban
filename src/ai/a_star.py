import heapq


def a_star(model, origin, destination, heuristic):
    def reconstruct_path(came_from, current):
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.append(current)
        return total_path[::-1]

    open_set = []
    heapq.heappush(open_set, (0, origin))

    came_from = {}
    g_score = {origin: 0}
    f_score = {origin: heuristic(origin, destination)}
    visited = []  # Lista para almacenar los nodos visitados en orden

    while open_set:
        current = heapq.heappop(open_set)[1]
        visited.append(current)  # Añadir el nodo actual a la lista de visitados

        if current == destination:
            path = reconstruct_path(came_from, current)
            return visited, path  # Retorna las posiciones visitadas y la ruta

        for neighbor in model.get_valid_move_neighbors(current):
            tentative_g_score = g_score[current] + 1  # Costo = 1 para cada paso
            if tentative_g_score < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, destination)
                if neighbor not in [i[1] for i in open_set]:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return visited, []
