import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 750
GRID_SIZE = 10
CELL_SIZE = 30
GRID_OFFSET_X = (WIDTH - GRID_SIZE * CELL_SIZE) // 2
GRID1_OFFSET_Y = 50
GRID2_OFFSET_Y = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battleships")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)

SHIPS = [5, 4, 3, 3, 2]

player1_board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
player2_board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
player1_view = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
player2_view = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

current_player = 1
placing_ships = True
current_ship = 0
ship_horizontal = True

def draw_grid(x_offset, y_offset, board, hide_ships=False, view_board=None):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x_offset + x * CELL_SIZE, y_offset + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 1)
            if board[y][x] == 1 and not hide_ships:
                pygame.draw.rect(screen, GRAY, rect)
            elif board[y][x] == 2:
                pygame.draw.circle(screen, RED, rect.center, CELL_SIZE // 2 - 5)
            elif view_board and view_board[y][x] == 3:
                miss_color = BLUE if y_offset == GRID2_OFFSET_Y else GREEN
                pygame.draw.line(screen, miss_color, (rect.left + 5, rect.top + 5), (rect.right - 5, rect.bottom - 5), 3)
                pygame.draw.line(screen, miss_color, (rect.right - 5, rect.top + 5), (rect.left + 5, rect.bottom - 5), 3)

def can_place_ship(board, x, y, size, horizontal):
    if horizontal:
        if x + size > GRID_SIZE:
            return False
        for i in range(size):
            if board[y][x + i] != 0:
                return False
    else:
        if y + size > GRID_SIZE:
            return False
        for i in range(size):
            if board[y + i][x] != 0:
                return False
    return True

def place_ship(board, x, y, size, horizontal):
    if horizontal:
        for i in range(size):
            board[y][x + i] = 1
    else:
        for i in range(size):
            board[y + i][x] = 1

def draw_ship_preview(x, y, size, horizontal, board, player):
    grid_y_offset = GRID1_OFFSET_Y if player == 1 else GRID2_OFFSET_Y
    grid_x = (x - GRID_OFFSET_X) // CELL_SIZE
    grid_y = (y - grid_y_offset) // CELL_SIZE
    if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
        if can_place_ship(board, grid_x, grid_y, size, horizontal):
            color = GREEN
        else:
            color = RED
        if horizontal:
            for i in range(min(size, GRID_SIZE - grid_x)):
                rect = pygame.Rect(GRID_OFFSET_X + (grid_x + i) * CELL_SIZE, grid_y_offset + grid_y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, color, rect, 2)
        else:
            for i in range(min(size, GRID_SIZE - grid_y)):
                rect = pygame.Rect(GRID_OFFSET_X + grid_x * CELL_SIZE, grid_y_offset + (grid_y + i) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, color, rect, 2)

def main():
    global placing_ships, current_player, current_ship, ship_horizontal
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)
        draw_grid(GRID_OFFSET_X, GRID1_OFFSET_Y, player1_board, current_player == 2, player2_view)
        draw_grid(GRID_OFFSET_X, GRID2_OFFSET_Y, player2_board, current_player == 1, player1_view)
        
        if placing_ships:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            board = player1_board if current_player == 1 else player2_board
            draw_ship_preview(mouse_x, mouse_y, SHIPS[current_ship], ship_horizontal, board, current_player)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and placing_ships:
                    ship_horizontal = not ship_horizontal
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                grid_y_offset = GRID1_OFFSET_Y if current_player == 1 or not placing_ships else GRID2_OFFSET_Y
                target_y_offset = GRID2_OFFSET_Y if current_player == 1 else GRID1_OFFSET_Y
                grid_x = (x - GRID_OFFSET_X) // CELL_SIZE
                grid_y = (y - grid_y_offset) // CELL_SIZE
                
                if placing_ships:
                    board = player1_board if current_player == 1 else player2_board
                    if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
                        is_horizontal = ship_horizontal if event.button == 1 else False
                        if can_place_ship(board, grid_x, grid_y, SHIPS[current_ship], is_horizontal):
                            place_ship(board, grid_x, grid_y, SHIPS[current_ship], is_horizontal)
                            current_ship += 1
                            if current_ship >= len(SHIPS):
                                current_ship = 0
                                current_player = 2 if current_player == 1 else 1
                                if current_player == 1:
                                    placing_ships = False
                else:
                    target_board = player2_board if current_player == 1 else player1_board
                    view_board = player1_view if current_player == 1 else player2_view
                    grid_y = (y - target_y_offset) // CELL_SIZE
                    if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE and event.button == 1:
                        if view_board[grid_y][grid_x] == 0:
                            if target_board[grid_y][grid_x] == 1:
                                view_board[grid_y][grid_x] = 2
                                target_board[grid_y][grid_x] = 2
                            else:
                                view_board[grid_y][grid_x] = 3
                            current_player = 2 if current_player == 1 else 1
        
        font = pygame.font.Font(None, 36)
        text = font.render(f"Player {current_player} placing ships ({SHIPS[current_ship]} cells)" if placing_ships else f"Player {current_player}'s Turn", True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, (GRID1_OFFSET_Y + GRID_SIZE * CELL_SIZE + GRID2_OFFSET_Y) // 2))
        screen.blit(text, text_rect)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()