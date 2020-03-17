

import pygame
import random as rnd
import time

from shape import S, Z, I, O, J, L, T, shapes, shape_colors

# Initializations
pygame.init()
pygame.font.init()
rnd.seed(int(time.time()))

LEVEL = 3
FPS = [48, 34, 24, 17, 10, 2]

# Display variables
WIDTH = 1000
HEIGHT = 800
PLAY_HEIGHT = HEIGHT
PLAY_WIDTH = PLAY_HEIGHT // 2
BLOCK_SIZE = PLAY_HEIGHT // 20
DELTA = (WIDTH - PLAY_WIDTH) // 2
DRAW_GRID = False # Weather to draw the grid or not
DRAW_OUTLINE = not DRAW_GRID # If the grid wont be drawn, each square will have an outline

# COLORS
BLACK = (0,0,0)
RED = (255,0,0)
WHITE = (255,255,255)

class Piece():

    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0
    
    def get_shape_rot(self):
        return self.shape[self.rotation % len(self.shape)]

    def render(self, surface):
        # Current shape according to rotation
        s = self.get_shape_rot()
        for coord in s:
            rect = (DELTA + (self.x+coord[0])*BLOCK_SIZE, (self.y-coord[1])*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(surface, self.color, rect)
            if DRAW_OUTLINE == True:
                pygame.draw.line(surface, WHITE, (rect[0], rect[1]), (rect[0], rect[1] + BLOCK_SIZE))
                pygame.draw.line(surface, WHITE, (rect[0], rect[1]), (rect[0] + BLOCK_SIZE, rect[1]))
                pygame.draw.line(surface, WHITE, (rect[0]+BLOCK_SIZE, rect[1]), (rect[0]+BLOCK_SIZE, rect[1]+BLOCK_SIZE))
                pygame.draw.line(surface, WHITE, (rect[0], rect[1]+BLOCK_SIZE), (rect[0]+BLOCK_SIZE, rect[1]+BLOCK_SIZE))

def get_piece():
    return Piece(5, 0, rnd.choice(shapes))

def move_piece(piece, table):
    # TODO check if the piece has landed
    global filled_pos

    piece.y += 1
    if check_pos_validity(piece, table) == True: # In this case it can't go down any more so the next piece follows
        piece.y -= 1
        for coord in piece.get_shape_rot():
            filled_pos[(piece.x + coord[0], piece.y - coord[1])] = piece.color
        return False
    return True
        
def out_of_bounds(piece):
    for coord in piece.get_shape_rot():
        if piece.y-coord[1] >= 20 or piece.x+coord[0] < 0 or piece.x+coord[0] >= 10:
            return True

    return False

def check_pos_validity(piece, table):
    
    # First check if it is out of bounds
    if out_of_bounds(piece):
        return True
    

def get_input(piece):
    # TODO add logic to check weather the piece can be moved/rotated
    global speed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        piece.x += 1
    if keys[pygame.K_LEFT]:
        piece.x -= 1
    if keys[pygame.K_DOWN]:
        speed = 2
    if keys[pygame.K_UP]:
        piece.rotation += 1

def draw_play_area(surface):
    
    if DRAW_GRID == True:
        pos_x = DELTA
        for x in range(9):
            pos_x += BLOCK_SIZE
            pygame.draw.line(surface, WHITE, (pos_x, 0), (pos_x, PLAY_HEIGHT))
        pos_y = 0
        for y in range(19):
            pos_y += BLOCK_SIZE
            pygame.draw.line(surface, WHITE, (DELTA, pos_y), (WIDTH - DELTA, pos_y))
    pygame.draw.line(surface, RED, (DELTA, 0), (DELTA, PLAY_HEIGHT), 4)
    pygame.draw.line(surface, RED, (WIDTH - DELTA, 0), (WIDTH - DELTA, PLAY_HEIGHT), 4)
    pygame.draw.line(surface, RED, (DELTA, PLAY_HEIGHT), (WIDTH - DELTA, PLAY_HEIGHT), 4)

def get_table(filled_pos={}): # filled_pos will contain key-value pairs which are composed of position-color

    table = [[BLACK for x in range(10)]  for x in range(20)]
    for row in range(20):
        for col in range(10):
            if (col, row) in filled_pos:
                table[row][col] = filled_pos[(col, row)]
    return table

def draw_table(surface, grid):
    
    pos_y = 0
    for row in range(20):
        pos_x = DELTA
        for col in range(10):
            rect = (pos_x, pos_y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(surface, grid[row][col], rect)
            pos_x += BLOCK_SIZE
        pos_y += BLOCK_SIZE

def update_display(surface, current_piece, table):

    surface.fill(BLACK) # Clear the display

    draw_table(surface, table) # Draws the currently placed pieces
    
    current_piece.render(surface)

    draw_play_area(surface)

    pygame.display.update()


def main(surface):

    global game_over, speed, filled_pos
    filled_pos = {}
    speed = 1
    game_over = False

    current_piece = get_piece()
    next_piece = get_piece()
    clock = pygame.time.Clock()
    frame = 0

    while not game_over:

        clock.tick(60) # Lock the frame rate at 60fps
        frame += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                get_input(current_piece)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    speed = 1
        
        table = get_table(filled_pos)
        if frame > FPS[LEVEL] // speed: # After every FPS[LEVEL]'th frame move the piece downwards
            if move_piece(current_piece, table) == False:
                current_piece = next_piece
                next_piece = get_piece()
            frame = 0
        update_display(surface, current_piece, table)


def main_menu():
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    main(window)

if __name__ == '__main__':
    main_menu()
    pygame.quit()
    exit()