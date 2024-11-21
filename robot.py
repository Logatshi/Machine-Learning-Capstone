class Robot(object):
    def __init__(self, maze_dim):
        """
        Initialize the robot with the size of the maze.

        Parameters:
        -----------
        maze_dim : int
            Dimension of the square maze (width and height).
        """
        self.maze_dim = maze_dim
        self.heading = 'up'
        self.location = [0, 0]
        self.visited = set()  # Keep track of visited cells
        self.visited.add(tuple(self.location))  # Add starting position to visited
        self.goal_bounds = [self.maze_dim // 2 - 1, self.maze_dim // 2]  # Center goal area

    def next_move(self, sensors):
        """
        Determine the robot's next rotation and movement based on sensor input.

        Parameters:
        -----------
        sensors : list of int
            Distances to obstacles on the left, front, and right of the robot.

        Returns:
        --------
        tuple of (rotation, movement)
            The rotation (in degrees) and the movement (in cells).
        """
        # Determine rotation based on sensor readings
        left, front, right = sensors

        # If there is a clear path ahead, move forward
        if front > 0:
            movement = 1
            rotation = 0
        elif left > 0:
            # Turn left if there's a clear path to the left
            movement = 1
            rotation = -90
        elif right > 0:
            # Turn right if there's a clear path to the right
            movement = 1
            rotation = 90
        else:
            # If all paths are blocked, turn around (180 degrees)
            movement = 0
            rotation = 90  # Turn right for now to attempt finding a new path

        # Update the robot's heading and location after deciding on a move
        self.update_position(rotation, movement)

        return rotation, movement

    def update_position(self, rotation, movement):
        """
        Update the robot's heading and position based on the movement and rotation.

        Parameters:
        -----------
        rotation : int
            The rotation angle (in degrees) of the robot.
        movement : int
            The movement (in cells) of the robot.
        """
        # Update the heading based on rotation
        self.heading = self.get_new_heading(rotation)

        # Move the robot forward based on the updated heading
        if movement > 0:
            if self.heading == 'up':
                self.location[1] += 1
            elif self.heading == 'right':
                self.location[0] += 1
            elif self.heading == 'down':
                self.location[1] -= 1
            elif self.heading == 'left':
                self.location[0] -= 1

        # Mark the new location as visited
        self.visited.add(tuple(self.location))

    def get_new_heading(self, rotation):
        """
        Get the new heading of the robot based on the current heading and rotation.

        Parameters:
        -----------
        rotation : int
            The rotation angle (in degrees) of the robot.

        Returns:
        --------
        str
            The updated heading direction.
        """
        headings = ['up', 'right', 'down', 'left']
        current_index = headings.index(self.heading)
        rotation_steps = rotation // 90
        new_index = (current_index + rotation_steps) % 4
        return headings[new_index]

    def is_at_goal(self):
        """
        Check if the robot has reached the goal area.

        Returns:
        --------
        bool
            True if the robot is at the goal area, False otherwise.
        """
        return (self.location[0] in self.goal_bounds and
                self.location[1] in self.goal_bounds)