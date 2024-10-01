import matplotlib.pyplot as plt
import numpy as np

def visualize_grid_world(file_path):
    """
    Visualizes a grid world loaded from a text file.

    Args:
        file_path (str): Path to the text file containing the grid world.
    """
    grid_world = []
    with open(file_path, 'r') as f:
        for line in f:
            row = list(line.strip())  # Create a list of characters
            for i in range(len(row)):
                if row[i] == '#':
                    row[i] = 2  # Blocked cells marked as 2
                else:
                    row[i] = int(row[i])  # Unblocked cells as 0 or 1
            grid_world.append(row)

    plt.figure()
    plt.imshow(np.array(grid_world), cmap='gray')
    plt.title(f'Grid World: {file_path}')
    plt.show()
    output_file = file_path.replace('.txt', '.png')
    plt.savefig(output_file)
    print(f'Grid World visualization saved to {output_file}')

def visualize_path(grid_world, path):
    """
    Visualizes the grid world with the path highlighted.
    
    Args:
        grid_world (list): 2D list representing the grid world.
        path (list): List of (x, y) tuples representing the path.
    """
    grid_copy = np.array(grid_world, dtype=int)

    for (x, y) in path:
        grid_copy[y][x] = 3  # Mark the path with a special value (e.g., 3)

    plt.figure()
    plt.imshow(grid_copy, cmap='gray')
    plt.title('Grid World with Path')
    plt.show()

# Example: Visualize 'grid_world_43.txt'
visualize_grid_world('grid_world_43.txt')
