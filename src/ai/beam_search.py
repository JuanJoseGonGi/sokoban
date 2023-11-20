from typing import Callable, List, Tuple, Optional


def beam_search(
    model,
    heuristic: Callable[[Tuple[int, int], Tuple[int, int]], float],
    beam_width: int,
    origin: Tuple[int, int],
    destination: Tuple[int, int],
) -> Tuple[List[Tuple[int, int]], Optional[List[Tuple[int, int]]]]:
    # Initialize the beam with the origin position
    beam = [(origin, [])]

    # Initialize the visited positions set
    visited_positions = []

    # Start the search loop
    while beam:
        # Expand the beam
        new_beam = []
        for position, path in beam:
            if position == destination:
                visited_positions.append(position)
                return visited_positions, path + [destination]

            # Add the current position to the visited set
            visited_positions.append(position)

            # Get the valid neighbors from the model
            valid_neighbors = model.get_valid_move_neighbors(position)

            # Generate new paths for each valid neighbor
            for new_position in valid_neighbors:
                if new_position not in visited_positions:
                    new_path = path + [new_position]
                    new_beam.append((new_position, new_path))

        # Sort the new beam based on the heuristic score and select the top beam_width positions
        new_beam.sort(key=lambda x: heuristic(x[0], destination))
        beam = new_beam[:beam_width]

    # If the destination is not reached, return None
    return visited_positions, None
