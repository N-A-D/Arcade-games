import os, sys
import pygame
from random import randint
from pygame.locals import *
from pygame.math import Vector2 as vec2D

if not pygame.font:
    print("Warning, fonts disabled!")
if not pygame.mixer: 
    print("Warning, sound disabled!")

WIN_SIZE = WIN_WIDTH, WIN_HEIGHT = 800, 800

BG_COLOR = (0, 0, 0)

TXT_COLOR = (52, 155, 235)

PADDLE_SPEED = 240
PADDLE_SIZE = PADDLE_WIDTH, PADDLE_HEIGHT = 10, 60
PADDLE_COLOR = (52, 155, 235)

BALL_SPEED = 250
BALL_SIZE = BALL_WIDTH, BALL_HEIGHT = 15, 15
BALL_COLOR = (52, 155, 235)

class PaddleOne(pygame.sprite.Sprite):
    def __init__(self, pos: vec2D):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.vel = vec2D(0, 0)
        self.image = pygame.Surface(PADDLE_SIZE)
        self.image.fill(PADDLE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self, dt: float):
        keys = pygame.key.get_pressed()
        self.vel = vec2D(0, 0)
        if keys[K_w]:
            self.vel.y = -PADDLE_SPEED
        elif keys[K_s]:
            self.vel.y = PADDLE_SPEED
        self.pos += self.vel * dt
        self.rect.center = self.pos
        if self.rect.bottom > WIN_HEIGHT:
            self.rect.bottom = WIN_HEIGHT
        elif self.rect.top < 0:
            self.rect.top = 0

class PaddleTwo(pygame.sprite.Sprite):
    def __init__(self, pos: vec2D):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.vel = vec2D(0, 0)
        self.image = pygame.Surface(PADDLE_SIZE)
        self.image.fill(PADDLE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self, dt: float):
        keys = pygame.key.get_pressed()

        self.vel = vec2D(0, 0)

        if keys[K_UP]:
            self.vel.y = -PADDLE_SPEED
        elif keys[K_DOWN]:
            self.vel.y = PADDLE_SPEED
        self.pos += self.vel * dt
        self.rect.center = self.pos

        if self.rect.bottom > WIN_HEIGHT:
            self.rect.bottom = WIN_HEIGHT
        elif self.rect.top < 0:
            self.rect.top = 0

class Ball(pygame.sprite.Sprite):
    def __init__(self, pos: vec2D, vel: vec2D):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.vel = vel
        self.image = pygame.Surface(BALL_SIZE)
        self.image.fill(BALL_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self, dt: float):
        self.pos += self.vel * dt
        self.rect.center = self.pos

        if self.rect.top < 0:
           self.rect.top = 0 
           self.vel.y = BALL_SPEED

        elif self.rect.bottom > WIN_WIDTH:
           self.rect.bottom = WIN_WIDTH
           self.vel.y = -BALL_SPEED

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(WIN_SIZE)
    pygame.display.set_caption("Pygame Pong")
    pygame.mouse.set_visible(False)

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(BG_COLOR)

    font = pygame.font.Font(None, 48)
    
    screen.blit(background, (0, 0))
    pygame.display.flip()

    clock = pygame.time.Clock()
    paddle_one = PaddleOne(vec2D(PADDLE_WIDTH, WIN_HEIGHT / 2))
    paddle_one_score = 0
    paddle_two = PaddleTwo(vec2D(WIN_WIDTH - PADDLE_WIDTH, WIN_HEIGHT / 2))
    paddle_two_score = 0
    ball = Ball(pos=vec2D(WIN_WIDTH / 2, BALL_HEIGHT), 
                vel=vec2D(randint(-BALL_SPEED, BALL_SPEED), BALL_SPEED))
    all_sprites = pygame.sprite.Group((paddle_one, paddle_two, ball))
    
    play = True
    while play:
        clock.tick(60)

        # event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                play = False

        # logic
        all_sprites.update(clock.get_time() / 1000)

        if pygame.sprite.collide_rect(paddle_one, ball):
            ball.vel.x = BALL_SPEED
        elif pygame.sprite.collide_rect(paddle_two, ball):
            ball.vel.x = -BALL_SPEED
        
        if ball.rect.right > WIN_WIDTH:
            ball.kill()
            paddle_one_score += 1
        
        elif ball.rect.left < 0:
            ball.kill()
            paddle_two_score += 1

        if not ball.alive():
            ball = Ball(pos=vec2D(WIN_WIDTH / 2, BALL_HEIGHT), 
                    vel=vec2D(randint(-BALL_SPEED, BALL_SPEED), BALL_SPEED))
            all_sprites.add(ball)

        if paddle_one_score == 11 or paddle_two_score == 11:
            play = False

        # drawing
        screen.blit(background, (0, 0))

        paddle_one_score_text = font.render(str(paddle_one_score), 1, TXT_COLOR)
        paddle_one_score_text_rect = paddle_one_score_text.get_rect()
        paddle_one_score_text_rect.center = (WIN_WIDTH / 8, WIN_HEIGHT / 12)
        screen.blit(paddle_one_score_text, paddle_one_score_text_rect)

        paddle_two_score_text = font.render(str(paddle_two_score), 1, TXT_COLOR)
        paddle_two_score_text_rect = paddle_two_score_text.get_rect()
        paddle_two_score_text_rect.center = (WIN_WIDTH - WIN_WIDTH / 8, WIN_HEIGHT / 12)
        screen.blit(paddle_two_score_text, paddle_two_score_text_rect)     
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()