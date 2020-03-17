

import pygame
import random as rnd
import time

from shape import S, Z, I, O, J, L, T, shapes, shape_colors

# Initializations
pygame.init()
pygame.font.init()
rnd.seed(int(time.time()))

LEVEL = 1
FPS = [48, 34, 24, 10, 2]

# Display variables
WIDTH = 1000
HEIGHT = 800
PLAY_HEIGHT = HEIGHT
PLAY_WIDTH = PLAY_HEIGHT // 2
BLOCK_SIZE = PLAY_HEIGHT // 20
DELTA = (WIDTH - PLAY_WIDTH) // 2
DRAW_GRID = True

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
    
    def render(self, surface):
        # Current shape according to rotation
        s = self.shape[self.rotation % len(self.shape)]
        for coord in s:
            rect = (DELTA + (self.x+coord[0])*BLOCK_SIZE, (self.y-coord[1])*BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(surface, self.color, rect)

def move_piece(piece):
    # TODO check if the piece has landed
    piece.y += 1

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

def draw_play_are(surface):
    
    if DRAW_GRID == True:
        dx = DELTA
        for x in range(9):
            dx += BLOCK_SIZE
            pygame.draw.line(surface, WHITE, (dx, 0), (dx, PLAY_HEIGHT))
        dy = 0
        for y in range(19):
            dy += BLOCK_SIZE
            pygame.draw.line(surface, WHITE, (DELTA, dy), (WIDTH - DELTA, dy))
    pygame.draw.line(surface, RED, (DELTA, 0), (DELTA, PLAY_HEIGHT), 4)
    pygame.draw.line(surface, RED, (WIDTH - DELTA, 0), (WIDTH - DELTA, PLAY_HEIGHT), 4)
    pygame.draw.line(surface, RED, (DELTA, PLAY_HEIGHT), (WIDTH - DELTA, PLAY_HEIGHT), 4)

def update_display(surface, current_piece):

    surface.fill(BLACK) # Clear the display

    current_piece.render(surface)

    draw_play_are(surface)

    pygame.display.update()


def main(surface):

    global game_over
    global speed
    speed = 1
    game_over = False

    current_piece = Piece(5, 0, T)
    clock = pygame.time.Clock()
    frame = 0

    while not game_over:

        clock.tick(60) # Set the frame rate
        frame += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                get_input(current_piece)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    speed = 1
        
        if frame > FPS[LEVEL] // speed: # After every FPS[LEVEL]'th frame move the piece downwards
            move_piece(current_piece)
            frame = 0
        update_display(surface, current_piece)


def main_menu():
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    main(window)

if __name__ == '__main__':
    main_menu()
    pygame.quit()
    exit()