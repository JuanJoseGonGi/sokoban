def load_map_file(path: str):
    with open(path, "r") as f:
        return f.read().splitlines()


def process_map_file_row(row: str):
    sanitized_row = (
        row.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")
    )
    map_file_row_agents = sanitized_row.split(",")
    map_file_row_agents = [agent for agent in map_file_row_agents if agent != ""]
    return map_file_row_agents


def process_map_file(map_file: list[str]):
    map_structure: dict[str, list[tuple[str, tuple[int, int]]]] = {
        "paths": [],
        "rocks": [],
        "goals": [],
        "robots": [],
        "boxes": [],
    }

    for y, map_file_row in enumerate(map_file):
        map_file_row_agents = process_map_file_row(map_file_row)
        for x, map_file_cell_agents in enumerate(map_file_row_agents):
            map_file_agents = map_file_cell_agents.split("-", 1)
            for map_file_agent in map_file_agents:
                upper_map_file_agent = map_file_agent.upper()
                if upper_map_file_agent == "C":
                    map_structure["paths"].append((upper_map_file_agent, (x, y)))
                elif upper_map_file_agent == "R":
                    map_structure["rocks"].append((upper_map_file_agent, (x, y)))
                elif upper_map_file_agent == "M":
                    map_structure["goals"].append((upper_map_file_agent, (x, y)))
                elif "B" in upper_map_file_agent:
                    map_structure["boxes"].append((upper_map_file_agent, (x, y)))
                elif "A" in upper_map_file_agent:
                    map_structure["robots"].append((upper_map_file_agent, (x, y)))

    return map_structure


if __name__ == "__main__":
    map_file = load_map_file("samples/map1.txt")
    map_structure = process_map_file(map_file)
    print(map_structure)
