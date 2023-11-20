from src.logic.sokoban import Sokoban


def dfs(model: Sokoban, origin: tuple[int, int], destination: tuple[int, int]):
    """Recursive implementation of DFS.

    It receives a model, an origin, and a destination, and returns a list
    of visited positions and a set of positions that form a path from the
    origin to the destination.
    """
    visited_positions = []
    path = set()

    def dfs_recursive(origin: tuple[int, int]):
        visited_positions.append(origin)
        if origin == destination:
            path.add(origin)
            return True
        for neighbor in model.get_valid_move_neighbors(origin):
            if neighbor not in visited_positions:
                if dfs_recursive(neighbor):
                    path.add(origin)
                    return True
        return False

    dfs_recursive(origin)
    return visited_positions, path
