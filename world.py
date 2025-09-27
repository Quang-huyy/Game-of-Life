from setting import INIT_GRASS
import pygame
import random

class World:
    def __init__(self, size):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.spawn_grass(init_grass = True)

    def random_position(self):
            while True:
                x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
                if self.grid[x][y] == None:
                    return x,y

    def spawn_grass(self, init_grass = False):
            if init_grass is True:
                nbr_grass = init_grass
            else:
                from setting import MIN_GRASS, MAX_GRASS
                nbr_grass = random.randint(MIN_GRASS, MAX_GRASS)
            for _ in range(nbr_grass):
                x, y = self.random_position()
                self.grid[x][y] = 'grass'

    def draw(self, screen):
        for x in range(self.size):
            for y in range(self.size):
                if self.grid[x][y] == 'grass':
                    from setting import CELL_WIDTH, CELL_HEIGHT, GRASS_COLOR
                    pygame.draw.rect(screen, GRASS_COLOR, rect=(x*CELL_WIDTH, y*CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))

    