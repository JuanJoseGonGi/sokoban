import os


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

    def process_map_file(
        self, map_file: list[str]
    ) -> tuple[dict[str, list[tuple[str, tuple[int, int]]]], int, int]:
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

    def map_structure_to_strings(
        self,
        map_structure: dict[str, list[tuple[str, tuple[int, int]]]],
    ) -> list[str]:
        width = 0
        height = 0

        # Obtener el ancho y alto del mapa
        for _, positions in map_structure.items():
            for _, position in positions:
                x, y = position
                if x > width:
                    width = x
                if y > height:
                    height = y

        width += 1
        height += 1

        # Inicializar una matriz de strings con 'C' para representar los caminos
        map_string_matrix = [["C" for _ in range(width)] for _ in range(height)]

        # Colocar rocas
        for rock in map_structure["rocks"]:
            x, y = rock[1]
            map_string_matrix[height - y - 1][x] = "R"

        # Colocar metas
        for goal in map_structure["goals"]:
            x, y = goal[1]
            map_string_matrix[height - y - 1][x] = "M"

        # Colocar cajas
        for box in map_structure["boxes"]:
            x, y = box[1]
            prefix = "C-"

            if map_string_matrix[height - y - 1][x] == "M":
                prefix = "M-"

            map_string_matrix[height - y - 1][x] = prefix + box[0].lower()

        # Colocar robots
        for robot in map_structure["robots"]:
            x, y = robot[1]
            prefix = "C-"

            if map_string_matrix[height - y - 1][x] == "M":
                prefix = "M-"

            map_string_matrix[height - y - 1][x] = prefix + robot[0].lower()

        # Convertir la matriz a una lista de strings
        map_strings = []
        for row in map_string_matrix:
            row_string = ", ".join(row) + ","
            map_strings.append(row_string)

        return map_strings

    def save_map_to_file(
        self,
        map_structure: dict[str, list[tuple[str, tuple[int, int]]]],
        path: str,
    ):
        map_strings = self.map_structure_to_strings(map_structure)

        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, "w") as f:
            for line in map_strings:
                f.write(line + "\n")


# Uso de los métodos para cargar y guardar el mapa
if __name__ == "__main__":
    loader = MapLoader()
    map_structure, width, height = loader.get_map_structure("samples/map2.txt")
    loader.save_map_to_file(map_structure, "samples/map1_saved.txt")
