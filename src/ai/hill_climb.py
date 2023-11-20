def hill_climb(model, origin, destination, heuristic):
    def backtrack(current, visited, path):
        # Retrocede en el camino hasta encontrar un nodo con vecinos no explorados
        for previous in reversed(path[:-1]):
            if any(
                neighbor not in visited
                for neighbor in model.get_valid_move_neighbors(previous)
            ):
                return previous
        return None  # No se encontró ningún camino viable

    current = origin
    path = [current]  # Inicializar el camino con la posición de origen
    visited = [current]  # Utilizar un conjunto para almacenar los nodos visitados

    while current != destination:
        neighbors = model.get_valid_move_neighbors(current)
        next_node = None
        next_node_score = float("inf")

        for neighbor in neighbors:
            if neighbor in visited:
                continue  # Ignorar los vecinos ya visitados

            score = heuristic(neighbor, destination)
            if score < next_node_score:
                next_node_score = score
                next_node = neighbor

        if next_node is None:
            # Intentar backtracking si no hay vecinos prometedores
            current = backtrack(current, visited, path)
            if current is None:
                # No hay camino viable
                return visited, path
        else:
            current = next_node
            visited.append(current)
            path.append(current)

    return visited, path
