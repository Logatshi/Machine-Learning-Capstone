from maze import Maze
from robot import Robot
import sys

# Global dictionaries for robot movement and sensing
DIRECTION_SENSORS = {
    'u': ['l', 'u', 'r'], 'r': ['u', 'r', 'd'],
    'd': ['r', 'd', 'l'], 'l': ['d', 'l', 'u'],
    'up': ['l', 'u', 'r'], 'right': ['u', 'r', 'd'],
    'down': ['r', 'd', 'l'], 'left': ['d', 'l', 'u']
}
DIRECTION_MOVE = {
    'u': [0, 1], 'r': [1, 0], 'd': [0, -1], 'l': [-1, 0],
    'up': [0, 1], 'right': [1, 0], 'down': [0, -1], 'left': [-1, 0]
}
DIRECTION_REVERSE = {
    'u': 'd', 'r': 'l', 'd': 'u', 'l': 'r',
    'up': 'd', 'right': 'l', 'down': 'u', 'left': 'r'
}

# Test and score parameters
MAX_TIME = 1000
TRAIN_SCORE_MULTIPLIER = 1 / 30.0

def run_simulation(maze_filename):
    """
    Run the robot simulation on the specified maze file.
    
    Parameters:
    -----------
    maze_filename : str
        The filename of the text file containing the maze data.
    """
    # Create a maze based on the input file
    maze = Maze(maze_filename)

    # Initialize the robot and set up its starting position
    robot = Robot(maze.dim)
    runtimes = []

    for run_number in range(2):
        print(f"\nStarting run {run_number + 1}...")

        # Initialize the robot's position and heading
        robot_position = {'location': [0, 0], 'heading': 'up'}
        total_time = 0
        run_active = True
        goal_reached = False

        while run_active:
            # Increment the total time for each step
            total_time += 1
            if total_time > MAX_TIME:
                run_active = False
                print("Time limit exceeded.")
                break

            # Get sensor readings for the current position and heading
            sensor_readings = [maze.dist_to_wall(robot_position['location'], direction)
                               for direction in DIRECTION_SENSORS[robot_position['heading']]]

            # Get the robot's action (rotation and movement)
            rotation, movement = robot.next_move(sensor_readings)

            # Debug information about the robot's decision
            print(f"Position: {robot_position['location']}, Heading: {robot_position['heading']}")
            print(f"Sensors: {sensor_readings}, Rotation: {rotation}, Movement: {movement}")

            # Handle reset conditions
            if (rotation, movement) == ('Reset', 'Reset'):
                if run_number == 0 and goal_reached:
                    runtimes.append(total_time)
                    print("Ending first run. Starting the next run...")
                    break
                else:
                    print("Cannot reset before reaching the goal.")
                    continue

            # Perform rotation
            robot_position['heading'] = perform_rotation(robot_position['heading'], rotation)

            # Perform movement
            if not move_robot(maze, robot_position, movement):
                print("Movement blocked by a wall.")

            # Check if the goal is reached
            if is_goal_reached(robot_position['location'], maze.dim):
                goal_reached = True
                if run_number == 1:
                    runtimes.append(total_time - sum(runtimes))
                    run_active = False
                    print(f"Goal reached! Run {run_number + 1} complete.")

    # Calculate and report the final score
    if len(runtimes) == 2:
        final_score = runtimes[1] + TRAIN_SCORE_MULTIPLIER * runtimes[0]
        print(f"Task complete! Score: {final_score:.3f}")

def perform_rotation(current_heading, rotation):
    """
    Update the robot's heading based on the specified rotation.
    
    Parameters:
    -----------
    current_heading : str
        The current direction the robot is facing.
    rotation : int
        The rotation angle (in degrees).
    
    Returns:
    --------
    str
        The updated direction the robot is facing.
    """
    if rotation == -90:
        return DIRECTION_SENSORS[current_heading][0]
    elif rotation == 90:
        return DIRECTION_SENSORS[current_heading][2]
    elif rotation == 0:
        return current_heading
    else:
        print("Invalid rotation value. No rotation performed.")
        return current_heading

def move_robot(maze, robot_position, movement):
    """
    Move the robot in the specified direction.
    
    Parameters:
    -----------
    maze : Maze
        The Maze object containing information about walls.
    robot_position : dict
        A dictionary containing the robot's current location and heading.
    movement : int
        The number of squares to move (-3 to 3).
    
    Returns:
    --------
    bool
        True if the robot moved successfully, False if it was blocked by a wall.
    """
    # Limit movement to a maximum of 3 squares per turn
    movement = max(min(int(movement), 3), -3)
    
    while movement:
        if movement > 0:
            if maze.is_permissible(robot_position['location'], robot_position['heading']):
                robot_position['location'][0] += DIRECTION_MOVE[robot_position['heading']][0]
                robot_position['location'][1] += DIRECTION_MOVE[robot_position['heading']][1]
                movement -= 1
            else:
                return False
        else:
            reverse_heading = DIRECTION_REVERSE[robot_position['heading']]
            if maze.is_permissible(robot_position['location'], reverse_heading):
                robot_position['location'][0] += DIRECTION_MOVE[reverse_heading][0]
                robot_position['location'][1] += DIRECTION_MOVE[reverse_heading][1]
                movement += 1
            else:
                return False
    return True

def is_goal_reached(location, maze_dim):
    """
    Check if the robot has reached the goal (center of the maze).
    
    Parameters:
    -----------
    location : list of int
        The robot's current location [x, y].
    maze_dim : int
        The dimension of the maze (width and height).
    
    Returns:
    --------
    bool
        True if the robot has reached the goal, False otherwise.
    """
    goal_range = [maze_dim // 2 - 1, maze_dim // 2]
    return location[0] in goal_range and location[1] in goal_range

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tester.py <maze_filename>")
    else:
        run_simulation(str(sys.argv[1]))