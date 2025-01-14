import pygame
import sys
import time
from algo.a_star import a_star
from algo.backtracking import backtracking
from algo.dijkstra import dijkstra
from algo.flood_fill import flood_fill 

from grids.hardcoded_grid import grid

pygame.init()

# Screen dimensions
screen_width, screen_height = 1200, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pathfinding Algorithms Menu")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.Font(None, 36)

# Menu options
menu_options = ["Run A* Algorithm", "Run Backtracking Algorithm", "Run Dijkstra Algorithm", "Run Flood Fill Algorithm", "Exit"]
selected_option = 0

# Start and end positions
start = (0, 0)  # Starting point in the grid
end = (len(grid) - 1, len(grid[0]) - 1)  # End point in the grid

def draw_menu():
    """
    Draws the main menu on the screen with options.
    Highlights the selected option in blue.
    """
    global selected_option
    
    screen.fill(WHITE)
    for index, option in enumerate(menu_options):
        color = BLUE if index == selected_option else BLACK
        text = font.render(option, True, color)
        text_rect = text.get_rect(center=(screen_width // 2, 150 + index * 50))
        screen.blit(text, text_rect)
    pygame.display.flip()

def draw_grid(grid):
    """
    Draws the grid on the screen, with black cells for obstacles and white for empty spaces.
    
    Args:
        grid (list): 2D list representing the grid layout.
    """
    rows = len(grid)
    cols = len(grid[0])
    cell_width = screen_width // cols
    cell_height = screen_height // rows
    for row in range(rows):
        for col in range(cols):
            color = BLACK if grid[row][col] == 1 else WHITE
            pygame.draw.rect(screen, color, (col * cell_width, row * cell_height, cell_width, cell_height))
            pygame.draw.rect(screen, BLUE, (col * cell_width, row * cell_height, cell_width, cell_height), 1)
    pygame.display.flip()

def draw_start_end():
    """
    Draws the start and end points on the grid.
    The start point is red, and the end point is blue.
    """
    draw_state(start, RED)
    draw_state(end, BLUE)

def draw_state(state, color):
    """
    Draws a single cell on the grid with the specified color.
    
    Args:
        state (tuple): Coordinates of the cell (row, col).
        color (tuple): RGB color value for the cell.
    """
    x, y = state
    cell_width = screen_width // len(grid[0])
    cell_height = screen_height // len(grid)
    pygame.draw.rect(screen, color, (y * cell_width, x * cell_height, cell_width, cell_height))
    pygame.display.flip()

def visualize_algorithm(algorithm, grid, start, end):
    """
    Visualizes the pathfinding algorithm step-by-step on the grid.
    
    Args:
        algorithm (function): Pathfinding algorithm to visualize.
        grid (list): 2D list representing the grid layout.
        start (tuple): Starting point coordinates (row, col).
        end (tuple): Ending point coordinates (row, col).
    """
    path = algorithm(grid, start, end)
    if not path:
        print("No path found!")
        return
    for position in path:
        draw_state(position, GREEN)
        time.sleep(0.1)

def handle_menu_input():
    """
    Handles the user's input for navigating the menu using arrow keys and selecting with Enter.
    
    Returns:
        selected_option (int): The currently selected menu option.
    """
    global selected_option
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_option = (selected_option - 1) % len(menu_options)
            elif event.key == pygame.K_DOWN:
                selected_option = (selected_option + 1) % len(menu_options)
            elif event.key == pygame.K_RETURN:
                return True  
    return False  

def main():
    running = True

    while running:
        draw_menu()
        selected = handle_menu_input()

        if selected:  
            if selected_option == len(menu_options) - 1:
                running = False
            else:
                screen.fill(WHITE)
                draw_grid(grid)
                draw_start_end()
                if selected_option == 0:
                    visualize_algorithm(a_star, grid, start, end)
                elif selected_option == 1:
                    visualize_algorithm(backtracking, grid, start, end)
                elif selected_option == 2:
                    visualize_algorithm(dijkstra, grid, start, end)
                elif selected_option == 3:
                    visualize_algorithm(flood_fill, grid, start, end)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
