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

def transpose(board):
    transposed = []
    for col_index in range(SIZE):
        new_row = []
        for row in board:
            new_row.append(row[col_index])
        transposed.append(new_row)
    return transposed

def reverse_rows(board):
    reversed_board = []
    for row in board:
        reversed_row = list(reversed(row))
        reversed_board.append(reversed_row)
    return reversed_board

def compress_row(row):
    new_row = []
    for value in row:
        if value != 0:
            new_row.append(value)
    changed = (len(new_row) != len(row))
    while len(new_row) < SIZE:
        new_row.append(0)
    return new_row, changed

def merge_row(row):
    score = 0
    new = row[:]
    for i in range(SIZE - 1):
        if new[i] != 0 and new[i] == new[i + 1]:
            new[i] = new[i] * 2
            new[i + 1] = 0
            score += new[i]
    return new, score

def move_left(board):
    moved = False
    score_gain = 0
    new_board = []
    for r in range(SIZE):
        row = board[r]
        compressed1, c1 = compress_row(row)
        merged, s = merge_row(compressed1)
        compressed2, c2 = compress_row(merged)
        new_board.append(compressed2)
        if c1 or c2 or compressed2 != row:
            moved = True
        score_gain += s
    return new_board, moved, score_gain

def move_right(board):
    reversed_board = reverse_rows(board)
    moved_board, moved, score = move_left(reversed_board)
    return reverse_rows(moved_board), moved, score

def move_up(board):
    trans = transpose(board)
    moved_board, moved, score = move_left(trans)
    return transpose(moved_board), moved, score

def move_down(board):
    trans = transpose(board)
    moved_board, moved, score = move_right(trans)
    return transpose(moved_board), moved, score

def possible_moves(board):
    for r in range(SIZE):
        for c in range(SIZE):
            if board[r][c] == 0:
                return True
    for r in range(SIZE):
        for c in range(SIZE-1):
            if board[r][c] == board[r][c+1]:
                return True
    for c in range(SIZE):
        for r in range(SIZE-1):
            if board[r][c] == board[r+1][c]:
                return True
    return False

def finish(text,score,h_score):
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.set_alpha(150)
    fade_surface.fill((0, 0, 0))
    screen.blit(fade_surface, (0, 0))
    win_text = BIG_FONT.render(f"{text}", True, (255, 255, 255))
    win_text_rect = win_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 40))
    screen.blit(win_text, win_text_rect)
    score_text = FONT.render(f"Your Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(score_text, score_rect)
    h_score_text = FONT.render(f"High Score: {h_score}", True, (255, 255, 255))
    h_score_rect = h_score_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 40))
    screen.blit(h_score_text, h_score_rect)
    restart_text = FONT.render("Press R to Restart", True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 80))
    screen.blit(restart_text, restart_rect)

def draw_board(board, score):
    screen.fill(BACKGROUND)
    title = BIG_FONT.render("2048", True, (119,110,101))
    screen.blit(title, (20, 20))
    score = FONT.render(f"Score: {score}", True, (119,110,101))
    screen.blit(score, (WIDTH - 150, 30))
    pygame.draw.rect(screen, GRID_BG, (MARGIN, BOARD_TOP, WIDTH - 2*MARGIN, WIDTH - 2*MARGIN), border_radius=8)
    tile_size = (WIDTH - 2*MARGIN - (SIZE+1)*MARGIN) // SIZE
    for r in range(SIZE):
        for c in range(SIZE):
            val = board[r][c]
            x = MARGIN + MARGIN + c*(tile_size+MARGIN)
            y = BOARD_TOP + MARGIN + r*(tile_size+MARGIN)
            rect = pygame.Rect(x, y, tile_size, tile_size)
            color = TILE_COLORS.get(val, EMPTY) if val!=0 else EMPTY
            pygame.draw.rect(screen, color, rect, border_radius=6)
            if val != 0:
                txt = FONT.render(str(val), True, (119,110,101) if val < 8 else (255,255,255))
                txt_rect = txt.get_rect(center=rect.center)
                screen.blit(txt, txt_rect)

def game_loop():
    board = new_board()
    score = h_score= 0
    add_random_tile(board)
    add_random_tile(board)
    running = True
    while running:
        moved = False
        gain = 0
        for event in pygame.event.get():
            if event.type == QUIT:
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
        if score>h_score:
            h_score=score
        flag = False
        for row in board:
            if 2048 in row:
                flag = True
                break
        if flag== True:
            text="You reached 2048!"
            finish(text,score,h_score)
        if not possible_moves(board):
            text="Game Over!"
            finish(text,score,h_score)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
if __name__ == "__main__":
    game_loop()
