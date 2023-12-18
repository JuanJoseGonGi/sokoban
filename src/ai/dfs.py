from typing import Callable, List, Tuple


def dfs(
    origin: Tuple[int, int],
    destination: Tuple[int, int],
    order: Tuple[str, str, str, str],
    is_valid_move_fn: Callable[
        [Tuple[int, int], Tuple[str, str, str, str]], List[Tuple[int, int]]
    ],
) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
    def dfs_recursive(
        current: Tuple[int, int],
        visited: List[Tuple[int, int]],
        path: List[Tuple[int, int]],
    ) -> bool:
        if current == destination:
            path.append(current)
            return True

        visited.append(current)

        for neighbor in is_valid_move_fn(current, order):
            if neighbor not in visited and dfs_recursive(neighbor, visited, path):
                path.append(current)
                return True

        return False

    visited_positions = []
    path = []
    dfs_recursive(origin, visited_positions, path)

    if not path:
        return list(visited_positions), []

    # Reverse the path to start from the origin
    path = path[::-1]

    # Counting column occurrences
    col_count: dict[int, int] = {}
    for pos in path:
        col = pos[1]  # Assuming the column is the second element of the tuple
        col_count[col] = col_count.get(col, 0) + 1

    # Finding the column with the most occurrences
    largest_col_key = max(col_count, key=lambda k: col_count[k])
    print("Column with most occurrences: " + str(largest_col_key))

    return list(visited_positions), path
