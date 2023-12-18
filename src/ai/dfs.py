from typing import Callable


def dfs(
    origin: tuple[int, int],
    destination: tuple[int, int],
    order: tuple[str, str, str, str],
    is_valid_move_fn: Callable[[tuple[int, int], tuple[str, str, str, str]], list],
):
    visited_positions = []
    path = []

    def dfs_recursive(current: tuple[int, int]):
        if current in visited_positions:
            return False

        visited_positions.append(current)
        if current == destination:
            path.append(current)
            return True

        for neighbor in is_valid_move_fn(current, order):
            if dfs_recursive(neighbor):
                path.append(current)
                return True

        return False

    dfs_recursive(origin)

    if len(path) == 0:
        return visited_positions, []

    # Calcular la columna más repetida en el path
    col_count: dict[int, int] = {}
    for pos in reversed(path):
        col = pos[1]  # Asumiendo que la columna es el segundo elemento de la tupla
        col_count[col] = col_count.get(col, 0) + 1

    # Encontrar la columna con más repeticiones
    largest_col_key = max(col_count, key=lambda k: col_count[k])

    print("Columna con más repeticiones: " + str(largest_col_key))

    return visited_positions, list(reversed(path))
