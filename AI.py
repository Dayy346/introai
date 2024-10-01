import random
import heapq
import numpy as np
import matplotlib.pyplot as plt

class Node:
    def __init__(self, x, y, g, h):
        self.x = x
        self.y = y
        self.g = g  # Cost from the start to this node
        self.h = h  # Heuristic (estimated cost to goal)
        self.f = g + h  # Total cost (f = g + h)
        self.parent = None  # To reconstruct the path later

    def __lt__(self, other):
        # Compare based on f-value, break ties by preferring larger g-values
        if self.f == other.f:
            return self.g > other.g  # Larger g-value preferred
        return self.f < other.f

def manhattan_heuristic(node, goal):
    return abs(node.x - goal[0]) + abs(node.y - goal[1])

def reconstruct_path(node):
    path = []
    while node:
        path.append((node.x, node.y))
        node = node.parent
    return path[::-1]  # Reverse path

def a_star_search(start, goal, grid):
    open_list = []
    closed_list = set()
    start_node = Node(start[0], start[1], 0, manhattan_heuristic(start, goal))
    heapq.heappush(open_list, start_node)

    while open_list:
        current_node = heapq.heappop(open_list)

        if (current_node.x, current_node.y) == goal:
            return reconstruct_path(current_node)  # Path found

        closed_list.add((current_node.x, current_node.y))

        # Get all valid neighbors (unblocked and within bounds)
        for neighbor_x, neighbor_y in get_neighbors(current_node, grid):
            if (neighbor_x, neighbor_y) in closed_list:
                continue

            neighbor_node = Node(neighbor_x, neighbor_y, current_node.g + 1, 
                                 manhattan_heuristic((neighbor_x, neighbor_y), goal))
            neighbor_node.parent = current_node
            heapq.heappush(open_list, neighbor_node)

    print("No path found")
    return None

def get_neighbors(node, grid):
    neighbors = []
    x, y = node.x, node.y
    if x > 0 and grid[y][x - 1] == '0':  # Left
        neighbors.append((x - 1, y))
    if x < len(grid[0]) - 1 and grid[y][x + 1] == '0':  # Right
        neighbors.append((x + 1, y))
    if y > 0 and grid[y - 1][x] == '0':  # Up
        neighbors.append((x, y - 1))
    if y < len(grid) - 1 and grid[y + 1][x] == '0':  # Down
        neighbors.append((x, y + 1))
    return neighbors

def adaptive_a_star(start, goal, grid, previous_search_g):
    """
    Adaptive A* updates the heuristic values after each search to reflect more accurate distances to the goal.
    """
    open_list = []
    closed_list = set()
    start_node = Node(start[0], start[1], 0, manhattan_heuristic(start, goal))
    heapq.heappush(open_list, start_node)

    while open_list:
        current_node = heapq.heappop(open_list)

        if (current_node.x, current_node.y) == goal:
            # After reaching the goal, update the h-values for all expanded nodes
            for node in closed_list:
                node.h = goal.g - node.g
            return reconstruct_path(current_node)  # Path found

        closed_list.add(current_node)

        for neighbor_x, neighbor_y in get_neighbors(current_node, grid):
            neighbor_node = Node(neighbor_x, neighbor_y, current_node.g + 1, 
                                 manhattan_heuristic((neighbor_x, neighbor_y), goal))
            neighbor_node.parent = current_node
            heapq.heappush(open_list, neighbor_node)

    print("No path found")
    return None

def generate_grid_world(width, height, blocked_probability):
    grid = [['#' for _ in range(width)] for _ in range(height)]  # '#' represents blocked cells
    stack = []
    current_x, current_y = random.randint(0, width - 1), random.randint(0, height - 1)
    grid[current_y][current_x] = '0'  # Start with an unblocked cell
    stack.append((current_x, current_y))

    while stack:
        neighbors = []
        if current_x > 0 and grid[current_y][current_x - 1] == '#':
            neighbors.append((current_x - 1, current_y))
        if current_x < width - 1 and grid[current_y][current_x + 1] == '#':
            neighbors.append((current_x + 1, current_y))
        if current_y > 0 and grid[current_y - 1][current_x] == '#':
            neighbors.append((current_x, current_y - 1))
        if current_y < height - 1 and grid[current_y + 1][current_x] == '#':
            neighbors.append((current_x, current_y + 1))

        if neighbors:
            next_x, next_y = random.choice(neighbors)
            if random.random() < 1 - blocked_probability:
                grid[next_y][next_x] = '0'  # Unblocked cell
                stack.append((next_x, next_y))
                current_x, current_y = next_x, next_y
            else:
                grid[next_y][next_x] = '1'  # Blocked cell
        else:  # Backtrack
            current_x, current_y = stack.pop()

    return grid

# Generate 50 grid worlds
for i in range(50):
    grid_world = generate_grid_world(101, 101, 0.3)

    # Store the grid world in a text file
    with open(f'grid_world_{i}.txt', 'w') as f:
        for row in grid_world:
            f.write(''.join(row) + '\n')
