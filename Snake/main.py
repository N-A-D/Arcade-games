# Classic snake arcade game
# Created by Ned Datiles

import sys
import pygame
from random import randint
from pygame.locals import *

WIN_SIZE = WIN_WIDTH, WIN_HEIGHT = 601, 601

CELL_SIZE = CELL_WIDTH, CELL_HEIGHT = 20, 20

BACKGROUND_COLOR = (0, 0, 0)
GRID_COLOR = (255, 255, 255)
TEXT_COLOR = GRID_COLOR

APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

SNAKE_SPEED = 50

class Block(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, color: tuple):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(CELL_SIZE)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

class Snake:
    def __init__(self):
        self.head = Block(( WIN_WIDTH / 2, WIN_HEIGHT / 2 ), SNAKE_COLOR)
        self.dir = (CELL_WIDTH, 0)
        self.segments = []

    def collides_with_itself(self) -> bool:
        for segment in self.segments:
            if pygame.sprite.collide_rect(self.head, segment):
                return True
        return False

    def add_segment(self):
        block = None
        if self.segments:
            block = Block(self.segments[-1].rect.topleft, SNAKE_COLOR)
        else:
            block = Block(self.head.rect.topleft, SNAKE_COLOR)
        self.segments.append(block)

    def update(self):
        if self.segments:
            for i in range(0, len(self.segments) - 1):
                self.segments[i] = self.segments[i + 1]
            block = Block(self.head.rect.topleft, SNAKE_COLOR)
            self.segments[-1] = block
        
        keys = pygame.key.get_pressed()
        
        if keys[K_UP]:
            self.dir = (0,-CELL_HEIGHT)
        elif keys[K_RIGHT]:
            self.dir = (CELL_WIDTH, 0)
        elif keys[K_DOWN]:
            self.dir = (0, CELL_HEIGHT)
        elif keys[K_LEFT]:
            self.dir = (-CELL_WIDTH, 0)
        topleft = self.head.rect.topleft
        self.head.rect.topleft = (topleft[0] + self.dir[0], topleft[1] + self.dir[1])

    def draw(self, screen: pygame.Surface):
        screen.blit(self.head.image, self.head.rect)
        for segment in self.segments:
            screen.blit(segment.image, segment.rect)

def draw_grid(screen: pygame.Surface):
    """
        Draws a grid onto the screen    
    """

    # draw vertical lines
    for i in range(0, WIN_WIDTH, CELL_WIDTH):
        pygame.draw.line(screen, GRID_COLOR, (0, i), (WIN_WIDTH, i))
    
    # draw horizontal lines
    for i in range(0, WIN_HEIGHT, CELL_HEIGHT):
        pygame.draw.line(screen, GRID_COLOR, (i, 0), (i, WIN_HEIGHT))

def make_apple():
    x = randint(0, int(WIN_WIDTH / CELL_WIDTH) - 1) * CELL_WIDTH
    y = randint(0, int(WIN_HEIGHT / CELL_HEIGHT) - 1) * CELL_HEIGHT
    return Block((x, y), APPLE_COLOR)

def draw_apple(apple: Block, screen: pygame.Surface):
    screen.blit(apple.image, apple.rect)

def snake_out_of_bounds(snake: Snake) -> bool:
    return (snake.head.rect.x < 0 
            or snake.head.rect.y < 0 
            or snake.head.rect.x > WIN_WIDTH - CELL_WIDTH
            or snake.head.rect.y > WIN_HEIGHT - CELL_HEIGHT)

def apple_collides_with_snake_head(apple: Block, snake: Snake) -> bool:
    return pygame.sprite.collide_rect(apple, snake.head)

def apple_collides_with_snake_body(apple: Block, snake: Snake) -> bool:
    for segment in snake.segments:
        if pygame.sprite.collide_rect(segment, apple):
            return True
    return False

def game_loop(screen: pygame.Surface):
    snake = Snake()
    apple = make_apple()

    clock = pygame.time.Clock()
    play = True
    game_over = False
    while play:
        clock.tick(10)

        # events
        for event in pygame.event.get():
            if event.type == QUIT:
                play = False

        # logic
        if apple_collides_with_snake_head(apple, snake):
            apple = make_apple()
            while apple_collides_with_snake_body(apple, snake):
                apple = make_apple()
            snake.add_segment()

        snake.update()

        if snake_out_of_bounds(snake) or snake.collides_with_itself():
            play = False
            game_over = True

        # rendering
        screen.fill(BACKGROUND_COLOR)
        draw_apple(apple, screen)
        snake.draw(screen)
        draw_grid(screen)
        pygame.display.flip()
    if game_over:
        game_over_loop(screen)

def game_over_loop(screen: pygame.Surface):
    done = False
    font = pygame.font.Font(None, 56)
    text = font.render("Game over. Press r to restart.", 1, TEXT_COLOR)
    text_rect = text.get_rect()
    text_rect.center = (WIN_WIDTH / 2, WIN_HEIGHT / 2)
    while not done:
        for event in pygame.event.get():
            if event.type == QUIT:
                done = True
            if event.type == KEYDOWN:
                if event.key == K_r:
                    game_loop(screen)

        screen.fill(BACKGROUND_COLOR)
        screen.blit(text, text_rect)
        pygame.display.flip()

def make_screen() -> pygame.Surface:
    screen = pygame.display.set_mode(WIN_SIZE)
    pygame.display.set_caption("Snake")
    pygame.mouse.set_visible(False)
    return screen

if __name__ == "__main__":
    pygame.init()
    game_loop(make_screen())
    pygame.quit()