import pygame

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set screen dimensions
WIDTH = 600
HEIGHT = 600
CELL_SIZE = 40
ROWS = HEIGHT // CELL_SIZE
COLS = WIDTH // CELL_SIZE

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wall Follower Algorithm Visualization")
clock = pygame.time.Clock()

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y))

def draw_state(state, color):
    pygame.draw.rect(screen, color, (state[1] * CELL_SIZE, state[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def get_neighbors(current_state, grid):
    neighbors = []
    x, y = current_state
    for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 1:
            neighbors.append((nx, ny))
    return neighbors

def wall_follower(start_state, goal_state, grid):
    current_state = start_state
    direction = (0, 1)  # Start facing right
    right_hand_rule = True
    backtrack_stack = []  # Stack to store previous states

    while current_state != goal_state:
        # Update visualization
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill(WHITE)
        draw_grid()
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col] == 0:
                    draw_state((row, col), BLACK)
                elif (row, col) == start_state:
                    draw_state((row, col), GREEN)
                elif (row, col) == goal_state:
                    draw_state((row, col), BLUE)
                elif (row, col) == current_state:
                    draw_state((row, col), RED)
        pygame.display.update()
        clock.tick(30)

        # Check right-hand side
        new_direction = (direction[1], -direction[0])
        next_state = (current_state[0] + new_direction[0], current_state[1] + new_direction[1])
        if next_state in get_neighbors(current_state, grid) and right_hand_rule:
            direction = new_direction
            current_state = next_state
        else:  # Move forward or switch to left-hand rule
            next_state = (current_state[0] + direction[0], current_state[1] + direction[1])
            if next_state in get_neighbors(current_state, grid):
                current_state = next_state
            else:  # Turn left if right is blocked or follow left-hand rule
                direction = (-direction[1], direction[0])
                next_state = (current_state[0] + direction[0], current_state[1] + direction[1])
                if next_state in get_neighbors(current_state, grid):
                    current_state = next_state
                elif right_hand_rule:  # Switch to left-hand rule
                    right_hand_rule = False
                    direction = (direction[1], -direction[0])  # Turn right
                    next_state = (current_state[0] + direction[0], current_state[1] + direction[1])
                    if next_state in get_neighbors(current_state, grid):
                        current_state = next_state
                    else:  # Stuck, backtrack
                        if backtrack_stack:
                            current_state = backtrack_stack.pop()  # Backtrack to last decision point
                        else:
                            return False  # No path found
                else:  # Stuck, backtrack
                    if backtrack_stack:
                        current_state = backtrack_stack.pop()  # Backtrack to last decision point
                    else:
                        return False  # No path found
        backtrack_stack.append(current_state)  # Store current state for backtracking
    return True

# Example usage:
grid = [
    [1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1],
    [0, 1, 0, 1, 1, 1],
    [1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 1]
]

start_state = (0, 0)
goal_state = (5, 5)

# success = wall_follower(start_state, goal_state, grid)
# if success:
#     print("Goal reached!")
# else:
#     print("No path to the goal.")