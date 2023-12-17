from typing import Callable, List, Tuple, Optional


def beam_search(
    model,
    heuristic: Callable[[Tuple[int, int], Tuple[int, int]], float],
    beam_width: int,
    origin: Tuple[int, int],
    destination: Tuple[int, int],
) -> Tuple[List[Tuple[int, int]], Optional[List[Tuple[int, int]]]]:
    # Initialize the beam with the origin position
    beam = [(origin, [origin])]

    visited_positions = []

    # Start the search loop
    while beam:
        new_beam = []
        for position, path in beam:
            visited_positions.append(position)

            if position == destination:
                #si encontro camino
                return visited_positions, path

            valid_neighbors = model.get_valid_move_neighbors(position)

            for new_position in valid_neighbors:
                if new_position not in visited_positions:
                    new_path = path + [new_position]
                    new_beam.append((new_position, new_path))

        # Sort the new beam based on the heuristic score and select the top beam_width positions
        new_beam.sort(key=lambda x: heuristic(x[0], destination))
        beam = new_beam[:beam_width]

    # If the destination is not reached, return None for the path
    return visited_positions, None
