

import pygame
import random as rnd
import time

from shape import S, Z, I, O, J, L, T, shapes, shape_colors

# Initializations
pygame.init()
pygame.font.init()
game_font = pygame.font.SysFont('Game font', 30)
rnd.seed(int(time.time())) # In order to not have the same pattern every game

LEVEL = 3
FPS = [48, 34, 24, 17, 10, 2]

COLUMN_COUNT = 10
ROW_COUNT = 20

# Display variables
WIDTH = 1000
HEIGHT = 800
PLAY_HEIGHT = HEIGHT
PLAY_WIDTH = PLAY_HEIGHT // 2
BLOCK_SIZE = PLAY_HEIGHT // ROW_COUNT
DELTA = (WIDTH - PLAY_WIDTH) // 2
DRAW_GRID = False # Weather to draw the grid or not
DRAW_OUTLINE = not DRAW_GRID # If the grid wont be drawn, each square will have an outline

# COLORS
BLACK = (0,0,0)
RED = (255,0,0)
WHITE = (255,255,255)
TURCUAZ = (64,224,208)
LILA = (124, 234, 2 )

class Piece():

    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0
    
    # Returns the shapes values list according to the current rotation
    def get_shape_rot(self):
        return self.shape[self.rotation % len(self.shape)]

    def render(self, surface):
        # Current shape according to rotation
        s = self.get_shape_rot()
        for coord in s:
            rect = (DELTA + (self.x+coord[0])*BLOCK_SIZE, (self.y-coord[1])*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(surface, self.color, rect)
            if DRAW_OUTLINE:
                pygame.draw.line(surface, WHITE, (rect[0], rect[1]), (rect[0], rect[1] + BLOCK_SIZE))
                pygame.draw.line(surface, WHITE, (rect[0], rect[1]), (rect[0] + BLOCK_SIZE, rect[1]))
                pygame.draw.line(surface, WHITE, (rect[0]+BLOCK_SIZE, rect[1]), (rect[0]+BLOCK_SIZE, rect[1]+BLOCK_SIZE))
                pygame.draw.line(surface, WHITE, (rect[0], rect[1]+BLOCK_SIZE), (rect[0]+BLOCK_SIZE, rect[1]+BLOCK_SIZE))

def get_piece():
    return Piece(5, -2, rnd.choice(shapes))

def drop_piece(piece, table):
    global filled_pos

    piece.y += 1
    if not pos_available(piece, table): # In this case it can't go down any more so the next piece follows
        piece.y -= 1
        for coord in piece.get_shape_rot():
            filled_pos[(piece.x + coord[0], piece.y - coord[1])] = piece.color
        return False
    return True

# Checks if the piece is going out of bounds    
def out_of_bounds(piece):
    # Check all the parts of the piece
    for coord in piece.get_shape_rot():
        if piece.y-coord[1] >= ROW_COUNT or piece.x+coord[0] < 0 or piece.x+coord[0] >= COLUMN_COUNT:
            return True
    return False

# Checks if the piece is colliding with anything inside the table
def collision_table(piece, table):
    for coord in piece.get_shape_rot():
        pos = (piece.x + coord[0], piece.y - coord[1])
        if pos[0] < 0 or pos[1] < 0:
            continue
        if table[pos[1]][pos[0]] != BLACK:
            return True
    return False

# Checks if  the piece can move to the given position
def pos_available(piece, table):
    
    # First check if it is out of bounds
    if out_of_bounds(piece):
        return False
    # Then check if it is colliding with a placed piece
    if collision_table(piece, table):
        return False
    # Other wise
    return True
    
def get_input(piece, table):

    global speed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        piece.x += 1
        if not pos_available(piece, table):
            piece.x -= 1
    if keys[pygame.K_LEFT]:
        piece.x -= 1
        if not pos_available(piece, table):
            piece.x += 1
    if keys[pygame.K_DOWN]:
        speed = 3
    if keys[pygame.K_UP]:
        piece.rotation += 1
        if not pos_available(piece, table):
            piece.rotation -= 1

            piece.x += 1
            piece.rotation += 1
            if not pos_available(piece, table):
                piece.x -= 1
                piece.rotation -=1

                piece.x -= 1
                piece.rotation += 1
                if not pos_available(piece, table):
                    piece.x += 1
                    piece.rotation -= 1

                    piece.x += 2
                    piece.rotation +=1
                    if not pos_available(piece, table):
                        piece.x -= 2
                        piece.rotation -= 1

                        piece.x -= 2
                        piece.rotation += 1
                        if not pos_available(piece, table):
                            piece.x += 2
                            piece.rotation -= 1     

def remove_row(table, row_to_remove, filled_pos):

    # Remove all the filled position above and including row_to_remove
    for row in range(0, row_to_remove+1):
        for col in range(COLUMN_COUNT):
            if (col, row) in filled_pos:
                filled_pos.pop((col, row))

    # Shift each row above the row_to_remove downwards by one
    for row in range(row_to_remove, 0, -1): 
        for col in range(COLUMN_COUNT):
            table[row][col] = table[row-1][col]
    
    # Add the new filled positions to filled_pos
    for row in range(row_to_remove, 0, -1):
        for col in range(COLUMN_COUNT):
            if table[row][col] != BLACK:
                filled_pos[(col, row)] = table[row][col]
    return table, filled_pos

def check_lines(table, filled_pos):

    for row in range(ROW_COUNT):
        full_row = True
        for col in range(COLUMN_COUNT):
            if table[row][col] == BLACK:
                full_row = False
                break
        if full_row:
            table, filled_pos = remove_row(table, row, filled_pos)
    return table, filled_pos

def is_game_over(row):
    for color in row:
        if color != BLACK:
            return True
    return False

def get_table(filled_pos={}): # filled_pos will contain position-color pairs

    table = [[BLACK for x in range(COLUMN_COUNT)]  for y in range(ROW_COUNT)]
    for row in range(ROW_COUNT):
        for col in range(COLUMN_COUNT):
            if (col, row) in filled_pos:
                table[row][col] = filled_pos[(col, row)]
    return table

def draw_play_area(surface):
    
    if DRAW_GRID:
        pos_x = DELTA
        for x in range(9):
            pos_x += BLOCK_SIZE
            pygame.draw.line(surface, WHITE, (pos_x, 0), (pos_x, PLAY_HEIGHT))
        pos_y = 0
        for y in range(19):
            pos_y += BLOCK_SIZE
            pygame.draw.line(surface, WHITE, (DELTA, pos_y), (WIDTH - DELTA, pos_y))
    pygame.draw.line(surface, LILA, (DELTA, 0), (DELTA, PLAY_HEIGHT), 4)
    pygame.draw.line(surface, LILA, (WIDTH - DELTA, 0), (WIDTH - DELTA, PLAY_HEIGHT), 4)
    pygame.draw.line(surface, LILA, (DELTA, PLAY_HEIGHT), (WIDTH - DELTA, PLAY_HEIGHT), 4)

def draw_table(surface, table):
    
    pos_y = 0
    for row in range(ROW_COUNT):
        pos_x = DELTA
        for col in range(COLUMN_COUNT):
            rect = (pos_x, pos_y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(surface, table[row][col], rect)
            if DRAW_OUTLINE and table[row][col] != BLACK:
                pygame.draw.line(surface, WHITE, (pos_x, pos_y), (pos_x+BLOCK_SIZE, pos_y))
                pygame.draw.line(surface, WHITE, (pos_x, pos_y), (pos_x, pos_y+BLOCK_SIZE))
                pygame.draw.line(surface, WHITE, (pos_x+BLOCK_SIZE, pos_y), (pos_x+BLOCK_SIZE, pos_y+BLOCK_SIZE))
                pygame.draw.line(surface, WHITE, (pos_x, pos_y+BLOCK_SIZE), (pos_x+BLOCK_SIZE, pos_y+BLOCK_SIZE))
            pos_x += BLOCK_SIZE
        pos_y += BLOCK_SIZE

def text_render(surface):
    
    next_piece_text = "Next piece:"
    size = game_font.size(next_piece_text)
    next_piece_text_render = game_font.render(next_piece_text, True, WHITE)
    surface.blit(next_piece_text_render, (WIDTH - DELTA//2 - size[0]//2, HEIGHT//3))

def update_display(surface, current_piece, next_piece, table):

    surface.fill(BLACK) # Clear the display

    text_render(surface) # Render game text
    next_piece.render(surface)

    draw_table(surface, table) # Draws the currently placed pieces
    current_piece.render(surface) # Render the current piece
    draw_play_area(surface) # Draw the play area

    pygame.display.update()

def main(surface):

    global game_over, speed, filled_pos
    filled_pos = {}
    speed = 1
    game_over = False

    current_piece = get_piece()
    next_piece = get_piece()
    next_piece.x = 13
    next_piece.y = 10
    clock = pygame.time.Clock()
    frame = 0

    while not game_over:

        clock.tick(60) # Lock the frame rate at 60fps
        frame += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                get_input(current_piece, table)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    speed = 1
        
        table = get_table(filled_pos)
        if is_game_over(table[0]):
            game_over = True
        table, filled_pos = check_lines(table, filled_pos)
        if frame >= FPS[LEVEL] // speed: # After every FPS[LEVEL]'th frame move the piece downwards
            if drop_piece(current_piece, table) == False: # If the piece cannot be moved then get the next one
                next_piece.x = 5
                next_piece.y = 0
                current_piece = next_piece
                next_piece = get_piece()
                next_piece.x = 13
                next_piece.y = 10
            frame = 0
        update_display(surface, current_piece, next_piece, table)

def main_menu():
    
    window = pygame.display.set_mode((WIDTH, HEIGHT))

    # Display menu text
    menu_font = pygame.font.SysFont('menu', 80, True)
    menu_text = 'PRESS ANY KEY TO START'
    menu_surface = menu_font.render(menu_text, 1, WHITE)
    text_size = menu_font.size(menu_text)
    window.blit(menu_surface, (WIDTH//2 - text_size[0]//2, HEIGHT//2 - text_size[1]//2))
    pygame.display.update()

    in_menu = True
    while in_menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                in_menu = False
    
    # Run the game
    main(window)

if __name__ == '__main__':
    main_menu()
    pygame.quit()
    exit()