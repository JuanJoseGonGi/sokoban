from typing import Callable, List, Tuple


def beam_search(
    heuristic: Callable[[Tuple[int, int], Tuple[int, int]], float],
    beam_width: int,
    origin: Tuple[int, int],
    destination: Tuple[int, int],
    order: Tuple[str, str, str, str],
    is_valid_move_fn: Callable[
        [Tuple[int, int], Tuple[str, str, str, str]], List[Tuple[int, int]]
    ],
) -> Tuple[List[Tuple[int, int]], List[Tuple[int, int]]]:
    # Initialize the beam with the origin position
    beam = [(origin, [origin])]
    visited_positions = [origin]

    while beam:
        new_beam = []
        for position, path in beam:
            if position == destination:
                return visited_positions, path

            valid_neighbors = is_valid_move_fn(position, order)

            for new_position in valid_neighbors:
                if new_position not in visited_positions:
                    visited_positions.append(new_position)
                    new_path = path + [new_position]
                    new_beam.append((new_position, new_path))

        # Efficiently create the new beam
        beam = sorted(new_beam, key=lambda x: heuristic(x[0], destination))[:beam_width]

    return visited_positions, []
