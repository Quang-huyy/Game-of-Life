import pygame
from setting import *
from world import World
from agents import Rabbit
def print_grid(grid):
    for i in range(len(world.grid)):
        print(world.grid[i])

pygame.init()
screen = pygame.display.set_mode(size=(WINDOW_HEIGHT, WINDOW_HEIGHT))
pygame.display.set_caption(title="Simulation Game")
clock = pygame.time.Clock()

world = World(GRID_SIZE)
rabbits = []
rabbit1 = Rabbit(world.random_position(), world)
rabbit1.gender = 'Male'
rabbits.append(rabbit1)
rabbit2 = Rabbit(world.random_position(), world)
rabbit2.gender = 'Female'
rabbits.append(rabbit2)
# rabbits = [Rabbit(world.random_position(), world) for _ in range(INIT_RABBIT)]
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BG_COLOR)
    world.draw(screen)
    world.spawn_grass()

    babies = []  # temporary storage
    for r in rabbits:
        if r.mate_cooldown <= 0:
            if r.gender == 'Male' or (r.gender == 'Female' and r.pregnant_time == 0):
                r.find_partner(world, rabbits)
        elif r.health <= 30:
            r.find_food(world, rabbits=rabbits)
        else:
            r.find_nothing(world, rabbits=rabbits)
        r.draw(screen)

    # Add all new rabbits after loop
    rabbits.extend(babies)

    pygame.display.flip()
    clock.tick(FPS)
# print_grid(grid=world.grid)

pygame.quit()