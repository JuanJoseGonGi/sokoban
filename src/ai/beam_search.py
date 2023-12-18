from typing import Callable, List, Tuple


def beam_search(
    heuristic: Callable[[Tuple[int, int], Tuple[int, int]], float],
    beam_width: int,
    origin: Tuple[int, int],
    destination: Tuple[int, int],
    order: Tuple[str, str, str, str],
    is_valid_move_fn: Callable[[tuple[int, int], tuple[str, str, str, str]], list],
) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
    # Initialize the beam with the origin position
    beam = [(origin, [origin])]

    visited_positions = []

    # Start the search loop
    while beam:
        new_beam = []
        for position, path in beam:
            visited_positions.append(position)
            if position == destination:
                return visited_positions, path

            valid_neighbors = is_valid_move_fn(position, order)

            for new_position in valid_neighbors:
                if new_position not in visited_positions:
                    new_path = path + [new_position]
                    new_beam.append((new_position, new_path))

        # Sort the new beam based on the heuristic score and select the top beam_width positions
        new_beam.sort(key=lambda x: heuristic(x[0], destination))
        beam = new_beam[:beam_width]

    return visited_positions, []
