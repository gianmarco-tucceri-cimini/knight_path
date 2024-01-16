import sys
from collections import deque
import graphviz

def is_valid_move(x, y, N):
    """
    Check if a move is valid on an N x N chessboard.

    Parameters:
    x (int): X-coordinate on the chessboard.
    y (int): Y-coordinate on the chessboard.
    N (int): Size of the chessboard.

    Returns:
    bool: True if the move is valid, False otherwise.
    """
    return 0 <= x < N and 0 <= y < N

def get_knight_moves(x, y, N):
    """
    Generate all possible moves for a knight from a given position.

    Parameters:
    x (int): Current X-coordinate of the knight.
    y (int): Current Y-coordinate of the knight.
    N (int): Size of the chessboard.

    Returns:
    list: A list of tuples representing valid moves.
    """
    moves = [
        (x + 2, y + 1), (x + 2, y - 1), 
        (x - 2, y + 1), (x - 2, y - 1),
        (x + 1, y + 2), (x + 1, y - 2), 
        (x - 1, y + 2), (x - 1, y - 2)
    ]
    return [(mx, my) for mx, my in moves if is_valid_move(mx, my, N)]

def bfs_shortest_path(start, end, N):
    """
    Find the shortest path(s) for a knight to move from start to end.

    Parameters:
    start (tuple): Starting position of the knight.
    end (tuple): Ending position of the knight.
    N (int): Size of the chessboard.

    Returns:
    list: A list containing all shortest paths.
    """
    queue = deque([([start], start)])
    visited = set()
    shortest_paths = []
    found_shortest_path_length = None

    while queue:
        path, current = queue.popleft()
        if current == end:
            if found_shortest_path_length is None:
                found_shortest_path_length = len(path)
            if len(path) == found_shortest_path_length:
                shortest_paths.append(path)
            continue

        if current in visited:
            continue
        visited.add(current)

        for move in get_knight_moves(current[0], current[1], N):
            if move not in visited:
                queue.append((path + [move], move))

    return shortest_paths

def format_path(path):
    """
    Format the path for display.

    Parameters:
    path (list): A list of tuples representing the path.

    Returns:
    str: A formatted string representation of the path.
    """
    return ' -> '.join([f"({x}, {y})" for x, y in path])

def generate_dot_file(shortest_paths, start, end):
    """
    Generate a DOT file and render it as a PNG image.

    Parameters:
    shortest_paths (list): A list containing all shortest paths.
    start (tuple): Starting position of the knight.
    end (tuple): Ending position of the knight.
    """
    dot = graphviz.Digraph(comment='Knight Shortest Paths')

    dot.node(str(start), shape='ellipse', color='green', label=f'Start {start}')
    dot.node(str(end), shape='ellipse', color='red', label=f'End {end}')

    for i, path in enumerate(shortest_paths, start=1):
        for j in range(len(path) - 1):
            dot.edge(str(path[j]), str(path[j + 1]), label=f'Step {j + 1} of Path {i}')

    dot.render('shortest_paths', format='png')

def main():
    """
    Main function to execute the knight pathfinding script.
    """
    if len(sys.argv) != 5:
        print("Usage: python knight_path.py <start_x> <start_y> <end_x> <end_y>")
        return

    start_x, start_y, end_x, end_y = map(int, sys.argv[1:])
    N = 8  # Size of the chessboard
    start = (start_x, start_y)
    end = (end_x, end_y)

    paths = bfs_shortest_path(start, end, N)
    if paths:
        print(f"\nFound {len(paths)} shortest path(s) from {start} to {end}:")
        for i, path in enumerate(paths, start=1):
            print(f"Path {i}: {format_path(path)} (Total Moves: {len(path)-1})")

        generate_dot_file(paths, start, end)
        print("Saved the 'shortest_paths.png' graph.")
    else:
        print(f"No paths found from {start} to {end}")

if __name__ == "__main__":
    main()
