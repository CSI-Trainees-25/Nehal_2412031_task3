#2048_game
import pygame
import random
from pygame.locals import *
pygame.init()
SIZE = 4
WIDTH = 500
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('2048 GAME')
clock = pygame.time.Clock()
FPS = 60
FONT = pygame.font.SysFont('Arial', 24, bold=True)
BIG_FONT = pygame.font.SysFont('Arial', 40, bold=True)
TILE_SIZE = 100
MARGIN = 15
BOARD_TOP = 120
BACKGROUND = (250,248,239)
GRID_BG = (187,173,160)
EMPTY = (205,193,180)
TILE_COLORS = {2: (238,228,218),4: (237,224,200),8: (242,177,121),16: (245,149,99),32: (246,124,95),64: (246,94,59),128: (237,207,114),256: (237,204,97),512: (237,200,80),1024: (237,197,63),2048: (237,194,46)}

def new_board():
    board = []
    for _ in range(SIZE):
        row = [0] * SIZE
        board.append(row)
    return board

def add_random_tile(board):
    empties = []
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] == 0:
                empties.append((r, c))
    if not empties:
        return False
    r, c = random.choice(empties)
    if random.random() < 0.1:
        board[r][c] = 4
    else:
        board[r][c] = 2
    return True

def move_left(board):
    pass

def move_right(board):
    pass

def move_up(board):
    pass

def move_down(board):
    pass

def possible_moves(board):
    pass

def draw_board(board, score):
    screen.fill(BACKGROUND)
    title = BIG_FONT.render("2048", True, (119,110,101))
    screen.blit(title, (20, 20))
    score = FONT.render(f"Score: {score}", True, (119,110,101))
    screen.blit(score, (WIDTH - 150, 30))
    pygame.draw.rect(screen, GRID_BG, (MARGIN, BOARD_TOP, WIDTH - 2*MARGIN, WIDTH - 2*MARGIN), border_radius=8)
    cell_size = (WIDTH - 2*MARGIN - (SIZE+1)*MARGIN) // SIZE
    for r in range(SIZE):
        for c in range(SIZE):
            val = board[r][c]
            x = MARGIN + MARGIN + c*(cell_size+MARGIN)
            y = BOARD_TOP + MARGIN + r*(cell_size+MARGIN)
            rect = pygame.Rect(x, y, cell_size, cell_size)
            color = TILE_COLORS.get(val, EMPTY) if val!=0 else EMPTY
            pygame.draw.rect(screen, color, rect, border_radius=6)
            if val != 0:
                txt = FONT.render(str(val), True, (119,110,101) if val < 8 else (255,255,255))
                txt_rect = txt.get_rect(center=rect.center)
                screen.blit(txt, txt_rect)

def game_loop():
    board = new_board()
    score = 0
    add_random_tile(board)
    add_random_tile(board)
    running = True
    while running:
        moved = False
        gain = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_q:
                    running = False
                elif event.key == K_r:
                    board = new_board()
                    score = 0
                    add_random_tile(board)
                    add_random_tile(board)
                elif event.key in (K_LEFT, K_a):
                    board2, moved, gain = move_left(board)
                elif event.key in (K_RIGHT, K_d):
                    board2, moved, gain = move_right(board)
                elif event.key in (K_UP, K_w):
                    board2, moved, gain = move_up(board)
                elif event.key in (K_DOWN, K_s):
                    board2, moved, gain = move_down(board)
                else:
                    board2 = board
                    moved = False
                    gain = 0
                if moved== True:
                    board = board2
                    score += gain
                    add_random_tile(board)
        draw_board(board, score)
        flag = False
        for row in board:
            if 2048 in row:
                flag = True
                break
        if flag== True:
            win_text = FONT.render("You reached 2048! (R to restart)", True, (0,128,0))
            screen.blit(win_text, (20, HEIGHT - 40))
        if not possible_moves(board):
            over_text = FONT.render("Game Over! (R to restart)", True, (128,0,0))
            screen.blit(over_text, (20, HEIGHT - 40))
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
if __name__ == "__main__":
    game_loop()
