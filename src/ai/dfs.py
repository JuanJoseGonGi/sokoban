def dfs(model, origin: tuple[int, int], destination: tuple[int, int]):
    visited_positions = []
    path = []

    def dfs_recursive(current: tuple[int, int]):
        if current in visited_positions:
            return False

        visited_positions.append(current)
        if current == destination:
            path.append(current)
            return True

        for neighbor in model.get_valid_move_neighbors(current):
            if dfs_recursive(neighbor):
                path.append(current)
                return True

        return False

    dfs_recursive(origin)

    # Calcular la columna más repetida en el path
    col_count: dict[int, int] = {}
    for pos in reversed(path):
        col = pos[1]  # Asumiendo que la columna es el segundo elemento de la tupla
        col_count[col] = col_count.get(col, 0) + 1

    # Encontrar la columna con más repeticiones
    largest_col_key = max(col_count, key=lambda k: col_count[k])

    print("Columna con más repeticiones: " + str(largest_col_key))

    return visited_positions, list(reversed(path))
