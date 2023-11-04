import random
import matplotlib.pyplot as plt
import numpy as np
from collections import deque


# 0 - Uncovered free block
# 1 - Uncovered blocked block
# 2 - Tower
# 3 - Covered free block
# 4 - Covered blocked block
class CityGrid:
    def __init__(self, rows, cols, block_percentage=30, tower_radius=1):
        self.rows = rows
        self.cols = cols
        self.tower_radius = tower_radius
        self.grid = self.generate_grid(block_percentage)

    def generate_grid(self, block_percentage):
        if block_percentage < 0 or block_percentage > 100:
            raise ValueError("Block percentage should be between 0 and 100")

        grid = [[0] * self.cols for _ in range(self.rows)]

        for row in range(self.rows):
            for col in range(self.cols):
                if random.randint(1, 100) <= block_percentage:
                    # 1 represents a blocked block
                    grid[row][col] = 1

        return grid

    def place_tower(self, row, col):
        if any([
            row < 0,
            col < 0,
            row >= self.rows,
            col >= self.cols,
            self.grid[row][col] in (1, 2, 4)
        ]):
            raise ValueError("Tower placement is invalid")

        '''
        Circle-like covering
        for r in range(max(0, row - tower_radius), min(self.rows, row + tower_radius + 1)):
            for c in range(max(0, col - tower_radius), min(self.cols, col + tower_radius + 1)):
                distance = (r - row) ** 2 + (c - col) ** 2
                if distance <= tower_radius ** 2:
                    self.grid[r][c] = 2  # 2 represents a tower coverage
        '''

        start_row = max(0, row - self.tower_radius)
        end_row = min(self.rows, row + self.tower_radius + 1)
        start_col = max(0, col - self.tower_radius)
        end_col = min(self.cols, col + self.tower_radius + 1)

        for r in range(start_row, end_row):
            for c in range(start_col, end_col):
                if self.grid[r][c] == 0:
                    self.grid[r][c] = 3
                elif self.grid[r][c] == 1:
                    self.grid[r][c] = 4

        self.grid[row][col] = 2

    def place_minimal_towers(self):
        uncovered_free_blocks = [
            (row, col)
            for row in range(self.rows)
            for col in range(self.cols)
            if self.grid[row][col] == 0
        ]

        available_for_placement_blocks = uncovered_free_blocks.copy()

        while uncovered_free_blocks:
            best_block = None
            max_coverage = 0

            for row, col in available_for_placement_blocks:
                coverage = 0

                # Assessing the coverage of a potential tower
                for r in range(max(0, row - self.tower_radius), min(self.rows, row + self.tower_radius + 1)):
                    for c in range(max(0, col - self.tower_radius), min(self.cols, col + self.tower_radius + 1)):
                        # Check if it is an uncovered free block
                        if self.grid[r][c] == 0:
                            coverage += 1

                if coverage > max_coverage:
                    max_coverage = coverage
                    best_block = (row, col)

            if best_block:
                row, col = best_block
                self.place_tower(row, col)

                # Override a list of all uncovered blocks and a list of all available for placement blocks
                uncovered_free_blocks = [(r, c) for r, c in uncovered_free_blocks if self.grid[r][c] == 0]
                available_for_placement_blocks.remove((row, col))

    def set_custom_grid(self, custom_grid):
        if len(custom_grid) != self.rows or any(len(row) != self.cols for row in custom_grid):
            raise ValueError("Invalid custom grid dimensions")

        for row in range(self.rows):
            for col in range(self.cols):
                cell_value = custom_grid[row][col]
                if cell_value not in (0, 1, 2, 3, 4):
                    raise ValueError("Invalid cell value in custom grid")
                self.grid[row][col] = cell_value

    def find_most_reliable_path(self, start_tower, end_tower):
        tower_graph = self.build_tower_graph()
        visited = set()
        queue = deque([(start_tower, 0)])
        distances = {start_tower: 0}
        predecessors = {}

        while queue:
            current, distance = queue.popleft()
            visited.add(current)

            if current == end_tower:
                break

            for neighbor in tower_graph[current]:
                if neighbor not in visited:
                    queue.append((neighbor, distance + 1))
                    visited.add(neighbor)
                    distances[neighbor] = distance + 1
                    predecessors[neighbor] = current

        path = []
        node = end_tower
        while node != start_tower:
            path.insert(0, node)
            node = predecessors[node]
        path.insert(0, start_tower)

        return path, distances[end_tower]

    def build_tower_graph(self):
        tower_graph = {}

        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == 2:
                    tower_coordinates = (row, col)
                    neighbors = []

                    for r in range(max(0, row - self.tower_radius), min(self.rows, row + self.tower_radius + 1)):
                        for c in range(max(0, col - self.tower_radius), min(self.cols, col + self.tower_radius + 1)):
                            if self.grid[r][c] == 2 and (r, c) != (row, col):
                                neighbor_coordinates = (r, c)
                                neighbors.append(neighbor_coordinates)

                    tower_graph[tower_coordinates] = neighbors

        return tower_graph

    def visualize_grid(self, start_tower=None, end_tower=None):
        # Using [::-1] to rotate the grid vertically,
        # since matplotlib considers the top-left corner as the starting coordinate
        grid_array = np.array(self.grid[::-1])
        cmap = plt.get_cmap("RdYlGn")

        fig, ax = plt.subplots()
        for row in range(self.rows):
            for col in range(self.cols):
                cell = grid_array[row, col]
                color = cmap(cell / 5)
                rect = plt.Rectangle(
                    (col, row),
                    1, 1,
                    facecolor=color,
                    edgecolor='black'
                )
                ax.add_patch(rect)

                if start_tower == (row, col):
                    # If the current cell is a start tower, highlight it with a red circle
                    circle = plt.Circle(
                        (col + 0.5, self.rows - row - 0.5),
                        0.4,
                        color='red',
                        fill=False,
                        zorder=2
                    )
                    ax.add_patch(circle)

                if end_tower == (row, col):
                    # If the current cell is an end tower, highlight it with a blue circle
                    circle = plt.Circle(
                        (col + 0.5, self.rows - row - 0.5),
                        0.4,
                        color='blue',
                        fill=False,
                        zorder=2
                    )
                    ax.add_patch(circle)

        ax.set_xticks(np.arange(self.cols))
        ax.set_yticks(np.arange(self.rows))
        ax.set_xticklabels([])
        ax.set_yticklabels([])

        if self.cols > self.rows:
            ax.set_xlim(0, self.cols)
            ax.set_ylim(0, self.cols)
        else:
            ax.set_xlim(0, self.rows)
            ax.set_ylim(0, self.rows)

        # Find and display the path
        if start_tower is not None and end_tower is not None:
            path, _ = self.find_most_reliable_path(start_tower, end_tower)
            path_x = [col + 0.5 for row, col in path]
            path_y = [self.rows - row - 0.5 for row, col in path]
            plt.plot(path_x, path_y, marker='o', color='purple')

        labels = [
            'Uncovered free blocks',
            'Uncovered blocked blocks',
            'Tower',
            'Covered free blocks',
            'Covered blocked blocks'
        ]
        legend_elements = [
            plt.Line2D(
                [0], [0],
                marker='o',
                color='w',
                label=labels[i],
                markersize=10,
                markerfacecolor=cmap(i / 5)
            )
            for i in range(5)
        ]
        ax.legend(handles=legend_elements, loc="upper right")

        plt.grid(True)
        plt.show()

    def __str__(self):
        result = ''
        for row in self.grid:
            result += ' '.join([str(cell) for cell in row]) + '\n'
        return result
