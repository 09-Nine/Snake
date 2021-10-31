import pygame
import sys
from pygame.math import Vector2
import random
import os
pygame.init()

CELL_SIZE = 30 
CELL_NUM = 20
FPS = 5
WIN = pygame.display.set_mode((CELL_SIZE * CELL_NUM, CELL_SIZE * CELL_NUM))
pygame.display.set_caption('SNAKE')
GAME_FONT = pygame.font.SysFont('comicsans', 100)

FRUIT_IMAGE = pygame.image.load(os.path.join('Assets', 'apple.png'))

#Color
RED_COLOR = (255, 0, 0)
SCREEN_COLOR = (175, 215, 70)

#Fruit
class Fruit:
    def __init__(self):
        self.x = random.randint(0, CELL_NUM-1)
        self.y = random.randint(0, CELL_NUM-1)
        self.pos = Vector2(self.x, self.y)

    def draw_fruits(self):
        fruit_rect = pygame.Rect(int(self.x * CELL_SIZE), int(self.y * CELL_SIZE), CELL_SIZE, CELL_SIZE)
        WIN.blit(FRUIT_IMAGE, fruit_rect)

    def reset(self):
        self.x = random.randint(0, CELL_NUM-1)
        self.y = random.randint(0, CELL_NUM-1)
        self.pos = Vector2(self.x, self.y)

#Snake
class Snake:
    def __init__(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(1, 0)
        self.add = False
        
        #snake image
        self.head_right = pygame.image.load(os.path.join('Assets', 'head_right.png'))
        self.head_left = pygame.image.load(os.path.join('Assets', 'head_left.png'))
        self.head_up = pygame.image.load(os.path.join('Assets', 'head_up.png'))
        self.head_down = pygame.image.load(os.path.join('Assets', 'head_down.png'))

        self.tail_right = pygame.image.load(os.path.join('Assets', 'tail_right.png'))
        self.tail_left = pygame.image.load(os.path.join('Assets', 'tail_left.png'))
        self.tail_down = pygame.image.load(os.path.join('Assets', 'tail_down.png'))
        self.tail_up = pygame.image.load(os.path.join('Assets', 'tail_up.png'))

        self.body_horizontal = pygame.image.load(os.path.join('Assets', 'body_horizontal.png'))
        self.body_vertical = pygame.image.load(os.path.join('Assets', 'body_vertical.png'))

        self.body_bl = pygame.image.load(os.path.join('Assets', 'body_bl.png'))
        self.body_br = pygame.image.load(os.path.join('Assets', 'body_br.png'))
        self.body_tl = pygame.image.load(os.path.join('Assets', 'body_tl.png'))
        self.body_tr = pygame.image.load(os.path.join('Assets', 'body_tr.png'))

    def draw_snake(self):
        self.control_head()
        self.control_tail()

        for index, block in enumerate(self.body):
            block_rect = pygame.Rect(block.x * CELL_SIZE, block.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if index == 0:
                WIN.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                WIN.blit(self.tail, block_rect)
            else:
                sub_next = self.body[index - 1] - block
                sub_previous = self.body[index + 1] - block
                
                if sub_previous.x == sub_next.x:
                    WIN.blit(self.body_vertical, block_rect)
                elif sub_next.y == sub_previous.y:
                    WIN.blit(self.body_horizontal, block_rect)
                else:
                    if sub_next.x == 1 and sub_previous.y == -1 or sub_next.y == -1 and sub_previous.x == 1:
                        WIN.blit(self.body_tr, block_rect) 
                    elif sub_next.x == -1 and sub_previous.y == -1 or sub_next.y == -1 and sub_previous.x == -1:
                        WIN.blit(self.body_tl, block_rect)
                    elif sub_next.x == 1 and sub_previous.y == 1 or sub_next.y == 1 and sub_previous.x == 1:
                        WIN.blit(self.body_br, block_rect)
                    elif sub_next.x == -1 and sub_previous.y == 1 or sub_next.y == 1 and sub_previous.x == -1:
                        WIN.blit(self.body_bl, block_rect)

    def control_head(self):
        head_relation = self.body[0] - self.body[1]

        if head_relation == Vector2(1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(0, 1):
            self.head = self.head_down
        elif head_relation == Vector2(0, -1):
            self.head = self.head_up

    def control_tail(self):
        tail_relation = self.body[-1] - self.body[-2]

        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_down
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_up

    def snake_move(self):

        if self.add == True:
            copy = self.body[:]
            copy.insert(0, copy[0] + self.direction)
            self.body = copy[:]
            self.add = False
        else:
            copy = self.body[:-1]
            copy.insert(0, copy[0] + self.direction)
            self.body = copy[:]

    def add_snake(self):
        self.add = True

    def reset(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(0, 0)

def check_game_over(snake):
    if not 0 <= snake.body[0].x < CELL_NUM or not 0 <= snake.body[0].y < CELL_NUM:
        return True
    
    for block in snake.body[1:]:
        if block == snake.body[0]:
            return True
    
    return False

def draw_game_text(text):
    draw_text = GAME_FONT.render(text, 1, RED_COLOR)
    WIN.blit(draw_text, (CELL_NUM*CELL_SIZE//2 - draw_text.get_width()//2, CELL_NUM*CELL_SIZE//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(2000)

def main():
    
    run = True
    fruit = Fruit()
    snake = Snake()
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key ==  pygame.K_RIGHT and snake.direction.x != -1:
                    snake.direction = Vector2(1, 0)
                if event.key == pygame.K_LEFT and snake.direction.x !=1:
                    snake.direction = Vector2(-1, 0)
                if event.key == pygame.K_UP and snake.direction.y != 1: 
                    snake.direction = Vector2(0, -1)
                if event.key == pygame.K_DOWN and snake.direction != -1:
                    snake.direction = Vector2(0, 1)
        
        if check_game_over(snake):
            draw_game_text('Game Over!!')
            run = False
        
        if snake.body[0] == fruit.pos:
            snake.add_snake()
            fruit.reset()
            for block in snake.body:
                if block == fruit.pos:
                    fruit.reset()

        WIN.fill(SCREEN_COLOR)
        fruit.draw_fruits()
        snake.draw_snake()
        snake.snake_move()
        pygame.display.update()
    
    pygame.quit()
    sys.exit()

if __name__ =='__main__':
    main()