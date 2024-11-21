import numpy as np

class Maze:
    """
    A class representing a maze.

    Attributes:
    -----------
    dim : int
        Dimension of the maze (it should be a square with even side length).
    walls : numpy.ndarray
        A 2D array representing the permeability of the walls in each cell.
        Each cell stores a 4-bit number to indicate the presence of walls.
    """

    def __init__(self, filename):
        """
        Initialize a Maze object from a file.

        Parameters:
        -----------
        filename : str
            The path to the file containing the maze's dimensions and wall data.

        Raises:
        -------
        Exception
            If the maze dimensions are not even or if there are inconsistencies 
            in the maze layout.
        """
        with open(filename, 'r') as f_in:
            # First line should be an integer with the maze dimensions
            self.dim = int(f_in.readline().strip())

            # Read subsequent lines to describe the permeability of walls
            walls = [list(map(int, line.strip().split(','))) for line in f_in]
            self.walls = np.array(walls)

        # Validate the maze's dimensions and wall permeability
        self._validate_maze()

    def _validate_maze(self):
        """
        Validate the dimensions and wall permeability of the maze.

        Raises:
        -------
        Exception
            If the maze's dimensions or wall permeability are invalid.
        """
        if self.dim % 2 != 0:
            raise Exception('Maze dimensions must be even in length!')

        if self.walls.shape != (self.dim, self.dim):
            raise Exception('Maze shape does not match dimension attribute!')

        wall_errors = []
        # Check vertical walls consistency
        for x in range(self.dim - 1):
            for y in range(self.dim):
                # Check if the right edge of the current cell matches the left edge of the next cell
                if (self.walls[x, y] & 2 != 0) != (self.walls[x + 1, y] & 8 != 0):
                    wall_errors.append([(x, y), 'v'])

        # Check horizontal walls consistency
        for y in range(self.dim - 1):
            for x in range(self.dim):
                # Check if the top edge of the current cell matches the bottom edge of the next cell
                if (self.walls[x, y] & 1 != 0) != (self.walls[x, y + 1] & 4 != 0):
                    wall_errors.append([(x, y), 'h'])

        # Report inconsistencies found
        if wall_errors:
            for cell, wall_type in wall_errors:
                if wall_type == 'v':
                    cell2 = (cell[0] + 1, cell[1])
                    print(f'Inconsistent vertical wall between {cell} and {cell2}')
                else:
                    cell2 = (cell[0], cell[1] + 1)
                    print(f'Inconsistent horizontal wall between {cell} and {cell2}')
            raise Exception('Consistency errors found in wall specifications!')

    def is_permissible(self, cell, direction):
        """
        Check if a cell is passable in a given direction.

        Parameters:
        -----------
        cell : list of int
            The coordinates of the cell as [x, y].
        direction : str
            The direction to check ('u', 'r', 'd', 'l' or full words).

        Returns:
        --------
        bool
            True if the cell is passable in the given direction, otherwise False.
        """
        dir_int = {'u': 1, 'r': 2, 'd': 4, 'l': 8, 'up': 1, 'right': 2, 'down': 4, 'left': 8}
        try:
            return bool(self.walls[tuple(cell)] & dir_int[direction])
        except KeyError:
            print('Invalid direction provided!')
            return False

    def dist_to_wall(self, cell, direction):
        """
        Calculate the distance from a cell to the nearest wall in a given direction.

        Parameters:
        -----------
        cell : list of int
            The coordinates of the cell as [x, y].
        direction : str
            The direction to check ('u', 'r', 'd', 'l' or full words).

        Returns:
        --------
        int
            The number of open cells until the nearest wall.
        """
        dir_move = {'u': [0, 1], 'r': [1, 0], 'd': [0, -1], 'l': [-1, 0],
                    'up': [0, 1], 'right': [1, 0], 'down': [0, -1], 'left': [-1, 0]}
        
        distance = 0
        current_cell = list(cell)  # Create a copy of the cell to avoid modifying the original

        while self.is_permissible(current_cell, direction):
            distance += 1
            current_cell[0] += dir_move[direction][0]
            current_cell[1] += dir_move[direction][1]

        return distance
