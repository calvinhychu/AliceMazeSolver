import sys

def not_visited(position, step_size, path_info, puzzle, visited):
    '''
    Return False if BFS has visited position with step_size or if the updated step_size(d) based
    on color of arrow in position is less than 1. Return True otherwise.
    If BFS has not visited position with step_size, it will update path_info to
    include the position and update d based on color of arrows in position.
    '''
    new_d = step_size
    if puzzle[position[0]][position[1]][0] == "yellow":
        new_d -= 1
    if (position, new_d) in visited:
        return False
    elif new_d < 1:
        return False
    else: # Not visited
        visited[(position, new_d)] = True
        path_info[1] = new_d # Update d
        path_info[0].append(position) # Update path
        return True


def check_goal(position, puzzle):
    '''
    Return True if position is the goal cell of puzzle. Return False otherwise.
    '''
    return puzzle[position[0]][position[1]][2]


def valid_moves(position, step_size, puzzle):
    '''
    Returns a list of valid moves from position and step_size in puzzle.
    '''
    result = []
    cell = puzzle[position[0]][position[1]]
    for direction in cell[1]:
        if direction == "N":
            x = position[0] - step_size
            y = position[1]
            if 0 <= x < maze_column_size:
                result.append((x, y))
        elif direction == "S":
            x = position[0] + step_size
            y = position[1]
            if 0 <= x < maze_column_size:
                result.append((x, y))
        elif direction == "E":
            x = position[0]
            y = position[1] + step_size
            if 0 <= y < maze_column_size:
                result.append((x, y))
        elif direction == "W":
            x = position[0]
            y = position[1] - step_size
            if 0 <= y < maze_column_size:
                result.append((x, y))
        elif direction == "NE":
            x = position[0] - step_size
            y = position[1] + step_size
            if 0 <= y < maze_column_size and 0 <= x < maze_column_size:
                result.append((x, y))
        elif direction == "NW":
            x = position[0] - step_size
            y = position[1] - step_size
            if 0 <= y < maze_column_size and 0 <= x < maze_column_size:
                result.append((x, y))
        elif direction == "SE":
            x = position[0] + step_size
            y = position[1] + step_size
            if 0 <= y < maze_column_size and 0 <= x < maze_column_size:
                result.append((x, y))
        elif direction == "SW":
            x = position[0] + step_size
            y = position[1] - step_size
            if 0 <= y < maze_column_size and 0 <= x < maze_column_size:
                result.append((x, y))
    return result


def find_shortest_path(puzzle, start_position):
    '''
    Main algorithm to run BFS. Prints shortest path from start_position to goal if one
    exists. Return True if there is a solution, False otherwise.
    '''
    result = ""
    d = 1
    step_count = 0
    init = [[start_position], d, step_count]
    queue = [init]
    visited = {}
    while len(queue) != 0:
        u = queue.pop(0)
        path = u[0]
        d = u[1]
        possible_moves = valid_moves(path[-1], d, puzzle) # path[-1] represents which cell the path is currently in
        for pos in possible_moves:
            new_u = [u[0].copy(), u[1], u[2]]  # create deepcopy
            if not_visited(pos, d, new_u, puzzle, visited):
                new_u[2] += 1 # Increment step count for that path
                path = new_u[0]
                if check_goal(path[-1], puzzle): # If path is able to reach the goal cell
                    step = new_u[2]
                    result = result + "Shortest Path: "
                    for i in range(len(path) - 1):
                        result = result + str(path[i]) + " --> "
                    result = result + str(path[-1]) + ", Steps: " + str(step)
                    print(result)
                    return True
                queue.append(new_u)
    print("Maze has no solution")
    return False


if len(sys.argv) != 2:
    print("Usage: python3 Alice.py <inputfilename>")
    sys.exit()

f = open(sys.argv[1])
maze_column_size = int(f.readline())
# Creating maze as an array from text representation of maze
maze = []
for i in range(maze_column_size):
    maze.append([])
# Read the starting position of maze
start_position = f.readline().split(", ")
start_position[0] = int(start_position[0])
start_position[1] = int(start_position[1])
start_position = tuple(start_position)

i = 0
line = f.readline()
# Filling in the detail of each cell of maze from text representation of maze
while line:
    temp = line.split("; ")
    temp[1] = temp[1].split(", ")
    temp[2] = temp[2].strip("\n")
    if temp[2] == "true": # True only if the cell is the goal cell of the maze
        temp[2] = True
    else:
        temp[2] = False
    maze[i // maze_column_size].append(temp)
    i += 1
    line = f.readline()
f.close()
start_cell = (maze[start_position[0]][start_position[1]])
find_shortest_path(maze, start_position) # Run the main algorithm to find shortest path