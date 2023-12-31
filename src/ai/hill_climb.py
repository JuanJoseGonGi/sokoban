def hill_climb(model, origin, destination, heuristic):
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
            # No hay vecinos prometedores, terminar la búsqueda
            break
        else:
            current = next_node
            visited.append(current)
            path.append(current)

    return visited, path
