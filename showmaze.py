import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.collections import PatchCollection
from maze import Maze
import sys

def plot_maze(maze_filename):
    """
    Visualize a maze using Matplotlib based on the walls in the maze.

    Parameters:
    -----------
    maze_filename : str
        The filename of the text file containing the maze data.
    """
    # Create the plot
    fig, ax = plt.subplots()

    # Load the maze data
    maze = Maze(maze_filename)

    # Extract walls and create rectangular patches for each wall
    wall_patches = extract_walls(maze)

    # Add wall patches to the plot
    ax.add_collection(PatchCollection(wall_patches, match_original=True))

    # Set plot properties
    set_plot_properties(ax, maze.dim)

    # Display the plot
    plt.show()

def extract_walls(maze):
    """
    Identify and create wall patches based on the maze's structure.

    Parameters:
    -----------
    maze : Maze
        The Maze object containing information about the maze's walls.

    Returns:
    --------
    list
        A list of Matplotlib patch objects representing walls.
    """
    walls = []

    for x in range(maze.dim):
        for y in range(maze.dim):
            if not maze.is_permissible([x, y], 'up'):
                walls.append(patches.Rectangle((x, y + 1), 1, 0.1, edgecolor='none'))
            if not maze.is_permissible([x, y], 'right'):
                walls.append(patches.Rectangle((x + 1, y), 0.1, 1, edgecolor='none'))
            if not maze.is_permissible([x, y], 'down'):
                walls.append(patches.Rectangle((x, y), 1, 0.1, edgecolor='none'))
            if not maze.is_permissible([x, y], 'left'):
                walls.append(patches.Rectangle((x, y), 0.1, 1, edgecolor='none'))

    return walls

def set_plot_properties(ax, maze_dim):
    """
    Set plot properties for displaying the maze.

    Parameters:
    -----------
    ax : matplotlib.axes.Axes
        The plot's axes object to set properties on.
    maze_dim : int
        The dimension of the maze (width and height).
    """
    ax.set_xlim(0, maze_dim)
    ax.set_ylim(0, maze_dim)
    ax.set_aspect('equal')
    plt.gca().invert_yaxis()

if __name__ == "__main__":
    # Check if the filename is provided
    if len(sys.argv) < 2:
        print("Usage: python showmaze.py <maze_filename>")
    else:
        plot_maze(str(sys.argv[1]))
