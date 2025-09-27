import random, pygame
from typing import List, Optional
import math
class Rabbit:
    def __init__(self, pos, world):
        self.x , self.y = pos
        self.update_world(world = world)
        from setting import MIN_HP, MAX_HP, RABBIT_GROW_TIME
        self.gender = random.choice(['Male', 'Female'])
        # if self.gender == 'Female':
        self.pregnant_time = 0
        self.health = random.randint(MIN_HP,MAX_HP)
        self.partner = False
        self.mate_time = 0
        self.mate_cooldown = RABBIT_GROW_TIME
        self.parents = []
        self.is_mating = False

    def update_world(self, world, old_x= None, old_y = None):
        world.grid[self.x][self.y] = 'rabbit'
        if old_x != None and old_y != None:
            world.grid[old_x][old_y] = None

    def wrap_position(self, x, y, world):
        return x % world.size, y % world.size

    def verify_step(self,new_x , new_y, rabbits: List["Rabbit"], findFood = True):
        if findFood:
            return all((new_x, new_y) != (r.x, r.y) for r in rabbits if r is not self)
        else:
            return True    

    def roam_around(self, world, rabbits: List["Rabbit"]):
        tries = 0
        new_x, new_y = old_x, old_y = self.x , self.y
        while(True):
            dx, dy = random.choice([-1, 0, 1]), random.choice([-1, 0, 1])
            new_x, new_y = self.wrap_position(self.x + dx, self.y + dy, world)
            if self.verify_step(new_x, new_y, rabbits):
                break
            tries +=1
            if tries > 10:
                break
        return new_x, new_y, old_x, old_y

    def step_finder(self, world, target, rabbits: List["Rabbit"],findFood = True):
        target_x, target_y = target
        step_x = 0
        step_y = 0
        if target_x > self.x:
            step_x = 1
        elif target_x < self.x:
            step_x = -1
        if target_y > self.y:
            step_y = 1
        elif target_y < self.y:
            step_y = -1

        new_x, new_y = self.wrap_position(self.x + step_x, self.y + step_y, world)
        if self.verify_step(new_x, new_y, rabbits, findFood):
            return new_x, new_y
        else:
            return self.x, self.y

    def make_child(self, world, new_x, new_y, partner: "Rabbit" = None):
        self.health -= 10
        from setting import MAX_NBR_CHILD
        for _ in range(MAX_NBR_CHILD):
            while True:
                pos = random.choice([new_x-1, new_x+1]), random.choice([new_y-1, new_y+1])
                if world.grid[pos[0]][pos[1]] == None:
                    from main import babies
                    new_rabbit = Rabbit(pos, world)
                    new_rabbit.parents = [self, partner]
                    babies.append(new_rabbit)
                    break

    def mating(self, partner: "Rabbit"):
        from setting import RABBIT_MATE_COOLDOWN, RABBIT_MATE_TIME, RABBIT_MATE_COST
        for r in (self, partner):
            r.is_mating = True
            r.health -= RABBIT_MATE_COST
            r.mate_time = RABBIT_MATE_TIME
            r.mate_cooldown = RABBIT_MATE_COOLDOWN
        self.partner = partner
        partner.partner = self

    def move(self,world, new_x, new_y, old_x = None, old_y= None, findFood = True, partner: "Rabbit" = None):
        print(self.mate_time)
        if self.gender == 'Female':
            print(f"pregant time: {self.pregnant_time}")
        #mating and pregnancy logic
        if self.is_mating:
            self.mate_time -= 1
            if self.mate_time <= 0:
                self.is_mating = False
                if self.partner:
                    self.partner.is_mating = False
                    self.partner.mate_time = 0

                    # Pregnancy when mating ends
                    from setting import RABBIT_PREGNANT_TIME
                    if self.gender == 'Female':
                        self.pregnant_time = RABBIT_PREGNANT_TIME
                    elif self.partner.gender == 'Female':
                        self.partner.pregnant_time = RABBIT_PREGNANT_TIME
        else:
            #find food
            if findFood:
                if world.grid[new_x][new_y] == 'grass':
                    self.health += 30
            #find mate
            else:
                if (new_x, new_y) == (partner.x, partner.y) and self.mate_cooldown == 0:
                    self.mating(partner)
                    return
                
            #update position
            self.x, self.y = new_x, new_y        
            if old_x != self.x or old_y != self.y:
                from setting import RABBIT_COST_PER_STEP
                self.health -= RABBIT_COST_PER_STEP

            #pregnancy
            if self.gender == 'Female':
                if self.pregnant_time > 0:
                    self.pregnant_time -=1
                elif self.pregnant_time == 0 and self.partner:
                    self.make_child(world, new_x, new_y, self.partner)
                    self.partner = None
            #mate cooldown
            if self.mate_cooldown > 0:
                self.mate_cooldown -= 1
        self.update_world(world = world, old_x= old_x, old_y= old_y)


    def find_food(self, world, rabbits: List["Rabbit"]): 
        old_x, old_y = self.x, self.y
        min_distance = math.inf
        target = None
        from setting import RABBIT_VISION
        for dx in  range(-RABBIT_VISION, RABBIT_VISION+1):
            for dy in range (-RABBIT_VISION, RABBIT_VISION+1):
                if not (dx == 0 and dy == 0):
                    new_x = (self.x + dx) % world.size
                    new_y = (self.y + dy) % world.size
                    if world.grid[new_x][new_y] == 'grass':
                        distance = abs(new_x - self.x) + abs(new_y - self.y)
                        if distance < min_distance:
                            min_distance = distance 
                            target = (new_x, new_y)
        if target:
            new_x, new_y = self.step_finder(world, target, rabbits)    
        else:
            new_x, new_y, old_x, old_y = self.roam_around(world, rabbits)
        self.move(world, new_x, new_y, old_x, old_y)

    def find_partner(self, world, rabbits: list["Rabbit"]):
        new_x, new_y = old_x, old_y = self.x, self.y
        target = None
        min_distance = math.inf
        from setting import RABBIT_VISION
        for dx in range(-RABBIT_VISION, RABBIT_VISION + 1):
            for dy in range(-RABBIT_VISION, RABBIT_VISION + 1):
                check_x = self.x + dx
                check_y = self.y + dy

                if 0 <= check_x < world.size and 0 <= check_y < world.size:
                    for r in rabbits:
                        if r is not self and (r.x, r.y) == (check_x, check_y):
                            if not r.partner and r.mate_cooldown == 0:
                                if self.gender == 'Male' and r.gender == 'Female' and r.pregnant_time == 0:
                                    # Male rabbits don't need to check pregnant_time
                                    distance = abs(dx) + abs(dy)
                                    if distance < min_distance:
                                        min_distance = distance
                                        target = r
                                elif self.gender == 'Female' and r.gender == 'Male':
                                    # Only consider females who are not pregnant
                                    if r.pregnant_time == 0:
                                        distance = abs(dx) + abs(dy)
                                        if distance < min_distance:
                                            min_distance = distance
                                            target = r
                                            print('partner found')

        if target:
            new_x, new_y = self.step_finder(world, (target.x, target.y), rabbits, findFood=False)
            self.move(world, new_x, new_y, old_x, old_y, findFood=False, partner=target)
        else:
            new_x, new_y, old_x, old_y = self.roam_around(world, rabbits)
            self.move(world, new_x, new_y, old_x, old_y, findFood=True)
        

    def find_nothing(self, world, rabbits: List["Rabbit"]):
        old_x, old_y = self.x, self.y
        new_x, new_y, old_x, old_y = self.roam_around(world, rabbits)
        self.move(world, new_x, new_y, old_x, old_y, findFood=True)


    def draw(self, screen):
        from setting import RABBIT_COLOR_MALE, RABBIT_COLOR_FEMALE, CELL_WIDTH, CELL_HEIGHT
        if self.gender == 'Male':
            pygame.draw.rect(screen, RABBIT_COLOR_MALE, (self.x*CELL_WIDTH, self.y*CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
        else:
            pygame.draw.rect(screen, RABBIT_COLOR_FEMALE, (self.x*CELL_WIDTH, self.y*CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))