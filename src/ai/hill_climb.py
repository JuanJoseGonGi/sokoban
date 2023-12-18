from typing import Callable, List, Tuple


def hill_climb(
    origin: Tuple[int, int],
    destination: Tuple[int, int],
    heuristic: Callable[[Tuple[int, int], Tuple[int, int]], float],
    order: Tuple[str, str, str, str],
    is_valid_move_fn: Callable[
        [Tuple[int, int], Tuple[str, str, str, str]], List[Tuple[int, int]]
    ],
) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
    current = origin
    path = [current]  # Initialize the path with the origin position
    visited = [current]

    while current != destination:
        neighbors = is_valid_move_fn(current, order)
        next_node = None
        next_node_score = float("inf")

        for neighbor in neighbors:
            if neighbor in visited:
                continue  # Skip already visited neighbors

            score = heuristic(neighbor, destination)
            if score < next_node_score:
                next_node_score = score
                next_node = neighbor

        if next_node is None:
            # No promising neighbors, end the search
            break
        else:
            current = next_node
            visited.append(current)
            path.append(current)

    return visited, path
