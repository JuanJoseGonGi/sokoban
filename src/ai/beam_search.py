from typing import Callable


def beam_search(
    model,
    heuristic: Callable[[tuple[int, int], tuple[int, int]], float],
    beam_width: int,
    origin: tuple[int, int],
    destination: tuple[int, int],
):
    """Recursive implementation of Beam Search.

    It receives a model, an heuristic function, a beam_width, an origin, and a destination, and returns a list
    of visited positions and a set of positions that form a path from the
    origin to the destination.
    """
    visited = []
    path = set()
    levels = {0: [origin]}

    def sorted_neighbors(neighborhood: list[tuple[int, int]]):
        return sorted(
            neighborhood,
            key=lambda neighbor: heuristic(neighbor, destination),
        )[:beam_width]

    def beam_search_recursive(level: int):
        visited.extend(levels[level])
        if destination in levels[level]:
            path.add(destination)
            return True

        neighborhood = []
        for position in levels[level]:
            for neighbor in model.get_valid_move_neighbors(position):
                if neighbor not in visited:
                    neighborhood.append(neighbor)
        neighborhood = sorted_neighbors(neighborhood)

        levels[level + 1] = neighborhood
        if len(levels[level + 1]) > 0:
            return beam_search_recursive(level + 1)
        return False

    return visited, path
