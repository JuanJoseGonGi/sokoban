class MapLoader:
    def load_map_file(self, path: str):
        with open(path, "r") as f:
            return f.read().splitlines()

    def process_map_file_row(self, row: str):
        sanitized_row = (
            row.replace(" ", "").replace("\t", "").replace("\n", "").replace("\r", "")
        )
        map_file_row_agents = sanitized_row.split(",")
        map_file_row_agents = [agent for agent in map_file_row_agents if agent != ""]
        return map_file_row_agents

    def process_map_file(self, map_file: list[str]):
        map_structure: dict[str, list[tuple[str, tuple[int, int]]]] = {
            "paths": [],
            "rocks": [],
            "goals": [],
            "robots": [],
            "boxes": [],
        }

        width = 0
        height = 0

        for y, map_file_row in enumerate(map_file):
            map_file_row_agents = self.process_map_file_row(map_file_row)
            if width < len(map_file_row_agents):
                width = len(map_file_row_agents)
            height += 1
            y_pos = len(map_file) - y - 1
            for x, map_file_cell_agents in enumerate(map_file_row_agents):
                map_file_agents = map_file_cell_agents.split("-", 1)
                for map_file_agent in map_file_agents:
                    upper_map_file_agent = map_file_agent.upper()
                    if upper_map_file_agent == "C":
                        map_structure["paths"].append(
                            (upper_map_file_agent, (x, y_pos))
                        )
                    elif upper_map_file_agent == "R":
                        map_structure["rocks"].append(
                            (upper_map_file_agent, (x, y_pos))
                        )
                    elif upper_map_file_agent == "M":
                        map_structure["goals"].append(
                            (upper_map_file_agent, (x, y_pos))
                        )
                    elif "B" in upper_map_file_agent:
                        map_structure["boxes"].append(
                            (upper_map_file_agent, (x, y_pos))
                        )
                    elif "A" in upper_map_file_agent:
                        map_structure["robots"].append(
                            (upper_map_file_agent, (x, y_pos))
                        )
                    else:
                        raise Exception(
                            f"Unknown map file agent: {upper_map_file_agent}"
                        )

        return map_structure, width, height

    def get_map_structure(self, path: str):
        map_file = self.load_map_file(path)
        return self.process_map_file(map_file)


if __name__ == "__main__":
    loader = MapLoader()
    map_structure, width, height = loader.get_map_structure("samples/map1.txt")
    print(map_structure, width, height)
