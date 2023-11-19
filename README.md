# Sokoban AI Project

## Overview

Sokoban is a classic puzzle game originating from Japan. The player (or in our case, a robot) needs to push boxes to specific locations in a warehouse. This project aims to implement Artificial Intelligence to solve the Sokoban puzzle by maneuvering the robot efficiently and moving all boxes to their target destinations within the simulated environment.

![Sokoban Image](./sokoban.jpg)

## Features

- Various Search Algorithms:
  - Breadth-First Search
  - Depth-First Search
  - Uniform Cost Search
  - Beam Search
  - Hill Climbing
  - A* Search
- Agents: Different types of agents that can be used to solve the puzzle.
  - Robot: Uses a simple pathfinding algorithm to move to the closest box, then pushes it to the closest target.
  - Wall: Blocks the path of the robot.
  - Floor: The robot can move freely on this tile.
  - Box: The robot can push this tile.
- World Simulation: An environment where agents interact, loadable from text files.
- Visualization: UI to visualize the pathfinding and box moving strategies.
- Customization: Different heuristic and search algorithm choices for the agent.

## Installation

### Prerequisites

- Python 3.x
- Pip (Python package manager)

### Steps

1. Clone the repository:

   ```sh
   git clone https://github.com/juanjosegongi/sokoban.git
   ```

2. Navigate to the project directory:

   ```sh
   cd sokoban
   ```

3. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Run the project:

   ```sh
   python main.py
   ```

## Usage

1. **Load the World**: Choose a pre-defined world or create your own using the provided examples.
2. **Choose an Algorithm**: Select the search algorithm and heuristic to be used by the agent.
3. **Simulate**: Watch the agent navigate and solve the puzzle, with paths and decisions visualized.

## Documentation

Detailed documentation on the usage, modules, and other aspects of the project can be found [here](./DOCUMENTATION.md).

## Testing

To run the tests, navigate to the project directory and run:

```sh
python -m unittest discover tests
```

## Contributing

Please read [CONTRIBUTING.md](link-to-your-contributing-md) for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- Reference to the original game or any inspired project if applicable.
- Acknowledge the authors, contributors, and users.
