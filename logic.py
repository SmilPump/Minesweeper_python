import random

# start int
ROWS, COLS, MINES = 9, 9, 10
board = []
visible = []
mine_positions = set()
first_click = True
game_over = False
win = False

def init_game(rows, cols, mines):
    global ROWS, COLS, MINES, board, visible, mine_positions, first_click, game_over, win
    ROWS = rows
    COLS = cols
    MINES = mines

    # board: 0 = empty, -1 = mine, 1+ = numbers
    board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    # visible: 0 = hidden, 1 = opened, 2 = flag
    visible = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    mine_positions = set()
    first_click = True
    game_over = False
    win = False

def generate_mines(first_r, first_c):
    global mine_positions
    # Blacklist the first clicked cell and its neighbors
    forbidden = {(first_r + dr, first_c + dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1]}

    while len(mine_positions) < MINES:
        r, c = random.randint(0, ROWS - 1), random.randint(0, COLS - 1)
        if (r, c) not in forbidden:
            mine_positions.add((r, c))
            board[r][c] = -1

    # Calculate neighbor numbers
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] == -1: continue
            count = sum(1 for dr in [-1, 0, 1] for dc in [-1, 0, 1]
                        if 0 <= r + dr < ROWS and 0 <= c + dc < COLS and board[r + dr][c + dc] == -1)
            board[r][c] = count


def reveal_cell(r, c):
    global game_over, win
    if visible[r][c] == 1 or visible[r][c] == 2: return
    visible[r][c] = 1

    # If hit a mine
    if board[r][c] == -1:
        global game_over
        for mr, mc in mine_positions: visible[mr][mc] = 1  # Show all bombs
        return

    # Auto-open empty neighbors using basic recursion
    if board[r][c] == 0:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS:
                    reveal_cell(nr, nc)
    check_win() #win moment

def check_win():
    global win, game_over
    for r in range(ROWS):
        for c in range(COLS):
            if board[r][c] != -1 and visible[r][c] != 1:
                return
    win = True
    game_over = True
