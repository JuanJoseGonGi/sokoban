def dfs(model, origin: tuple[int, int], destination: tuple[int, int]):
    """Recursive implementation of DFS.

    It receives a model, an origin, and a destination, and returns a list
    of visited positions and a set of positions that form a path from the
    origin to the destination.
    """
    visited_positions = []
    path = []

    def dfs_recursive(origin: tuple[int, int]):
        visited_positions.append(origin)
        if origin == destination:
            path.append(origin)
            return True
        for neighbor in model.get_valid_move_neighbors(origin):
            if neighbor not in visited_positions:
                if dfs_recursive(neighbor):
                    path.append(origin)
                    return True
        return False

    dfs_recursive(origin)

    # 2. Most repeated column index in answer
    col_count: dict[int, int] = {}
    largest_col_key = 0

    print("path", path)

    for pos in path:
        col = pos[0]
        if not col_count.get(col):
            col_count[col] = 1
            continue

        col_count[col] += 1
        largest_col_key = col

    for key in col_count:
        possible_largest = col_count.get(key)
        if not possible_largest:
            continue

        current_largest = col_count.get(largest_col_key)
        if not current_largest:
            largest_col_key = key
            continue

        if possible_largest >= current_largest:
            largest_col_key = key

    print("Columna con más repeticiones: " + str(largest_col_key))

    return visited_positions, path
