import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font('arial.ttf', 25)


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
MIN_SPEED = 10
MAX_SPEED = 30

class SnakeGame:

    def __init__(self, w=2000, h=1000):
        self.w = w
        self.h = h
        self.gameSpeed = 10
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('RacingSim')
        self.clock = pygame.time.Clock()
        self.track = [Point(50,5), Point(51,5)]
        print(self.track)
        i = 0
        for point in self.track:
            x = point.x
            y = point.y
            x *= BLOCK_SIZE
            y *= BLOCK_SIZE
            self.track[i] = Point(x, y)
            i+=1
        print(self.track)


        # init game state
        self.direction = Direction.RIGHT

        self.car = Point(self.w / 2, self.h / 2)

        self.score = 0
        self.food = None


    def play_step(self):
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        # 2. move
        keys = pygame.key.get_pressed()
        nothingDone = True
        if keys[pygame.K_LEFT]:
            self.direction = Direction.LEFT
            self._move(self.direction)
            nothingDone = False
        if keys[pygame.K_RIGHT]:
            self.direction = Direction.RIGHT
            self._move(self.direction)
            nothingDone = False
        if keys[pygame.K_UP]:
            self.direction = Direction.UP
            self._move(self.direction)
            nothingDone = False
        if keys[pygame.K_DOWN]:
            self.direction = Direction.DOWN
            self._move(self.direction)
            nothingDone = False
        if nothingDone:
            if self.gameSpeed > MIN_SPEED:
                print("tu")
                self.gameSpeed -= 3
        print(self.gameSpeed)
        # 2. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score


        # 4. update ui and clock
        self._update_ui()
        self.clock.tick(self.gameSpeed)
        # 5. return game over and score
        return game_over, self.score

    def _is_collision(self):
        # hits boundary
        if self.car.x > self.w - BLOCK_SIZE or self.car.x < 0 or self.car.y > self.h - BLOCK_SIZE or self.car.y < 0:
            return True
        elif self.car in self.track:
            return True
        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        pygame.draw.rect(self.display, RED, pygame.Rect(self.car.x, self.car.y, BLOCK_SIZE, BLOCK_SIZE))

        for pt in self.track:
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Lap: " + str(self.score) + "/57", True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, direction):
        x = self.car.x
        y = self.car.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        self.car = Point(x, y)
        if self.gameSpeed < MAX_SPEED:
            self.gameSpeed += 1

if __name__ == '__main__':
    game = SnakeGame()

    # game loop
    while True:
        game_over, score = game.play_step()

        if game_over == True:
            break

    print('Final Score', score)

    pygame.quit()