
import math
import pygame
import random

width = 8
height = 40
MAX_SPEED = 20
acceleration = 0.02
rotation_velocity = 5

class DNA(object):

    def __init__(self, frames):
        self.genes = []
        for _ in range(frames):
            # (rotate, accelerate)
            #rotate: 0 = rotateLeft, 1=no rotation 2 = rotate right
            #accelerate: 0=dont 1=accelerate
            self.genes.append((random.randrange(0,3), random.randrange(0,2)))

    def mutate(self, mutation_rate):
        for i in range(len(self.genes)):
            if(random.uniform(0,1) <= mutation_rate):
                self.genes[i] = (random.randrange(0,3), random.randrange(0,2))
        
    def crossover(self, element):
        child = DNA(len(self.genes))
        crossover_index = random.randrange(0, len(self.genes))
        for i in range(crossover_index):
            child.genes[i] = element.genes[i]
        for i in range(crossover_index,  len(self.genes)):
            child.genes[i] = self.genes[i]
        return child

class Rocket(object):
    
    def __init__(self, pos_x, pos_y, frames, window_width, window_height,
     target_x, target_y, obstacle, dna=0):
        self.x = pos_x
        self.y = pos_y - height
        self.width = width
        self.height = height
        self.velocity_x = 0
        self.velocity_y = 0
        self.rotation = 180
        self.target_x = target_x
        self.target_y = target_y
        self.completed = False
        self.obstacle = obstacle
        self.crashed = False
        if dna == 0:
            self.dna = DNA(frames)
        else:
            self.dna = dna

        self.window_height = window_height
        self.window_width = window_width

        self._image_orig = pygame.Surface((self.width, self.height))
        self._image_orig.set_colorkey((0,0,0))
        self._image_orig.fill((255,0,0))
        self._image = self._image_orig.copy()
        self._image.set_colorkey((0,0,0))
        self._rect = self._image.get_rect()
        self._rect.center = (self.x, self.y)

        self.fitness = 0

    def random(self):
        self.rotation = random.randrange(90, 270)
        self.velocity_x += math.sin(math.pi/180 * self.rotation) * 5
        self.velocity_y += math.cos(math.pi/180 * self.rotation) * 5

    def rotateLeft(self):
        self.rotation += rotation_velocity
        self.rotation %= 360
        # print("rotation: {}".format(self.rotation))
    
    def rotateRight(self):
        self.rotation -= rotation_velocity
        self.rotation %= 360
        # print("rotation: {}".format(self.rotation))

    def accelerate(self):
        self.velocity_x += math.sin(math.pi/180 * self.rotation) * acceleration
        self.velocity_y += math.cos(math.pi/180 * self.rotation) * acceleration

        if self.velocity_x > MAX_SPEED:
            self.velocity_x = MAX_SPEED
        if self.velocity_y > MAX_SPEED:
            self.velocity_y = MAX_SPEED

        # print("velocity_x: {}".format(self.velocity_x))
        # print("velocity_y: {}".format(self.velocity_y))

    def draw(self, window):
        new_image = pygame.transform.rotate(self._image_orig, self.rotation)
        rect = new_image.get_rect()
        rect.center = (self.x, self.y)
        window.blit(new_image, rect)

    def applyDNA(self, count):

        if count < len(self.dna.genes):
            (rotate, accelerate) = self.dna.genes[count]
            # print("accelerate: {}".format(accelerate))
            if rotate == 0:
                self.rotateLeft()
            if rotate == 2:
                self.rotateRight()
            if accelerate == 1:
                self.accelerate()

    def update(self, count):

        if (self.x > self.obstacle.x and self.x < self.obstacle.x + self.obstacle.width and
        self.y > self.obstacle.y and self.y < self.obstacle.y + self.obstacle.height):
            self.crashed = True
        
        if self.crashed:
            return

        dist = math.sqrt( (self.x- self.target_x)**2 + (self.y - self.target_y) **2)

        if(dist < 10):
            self.completed = True

        if not self.completed:
            self.applyDNA(count)

            self.x += self.velocity_x
            self.y += self.velocity_y

        

    def offscreen(self):

        if self.x > self.window_width or self.x < 0:
            return True
        if self.y > self.window_height or self.y < 0:
            return True
        return False


    def calcFitness(self):
        dist = math.sqrt( (self.x- self.target_x)**2 + (self.y - self.target_y) **2)
        print("distance: {}".format(dist))

        self.fitness = (1 / dist)
        if self.completed:
            self.fitness *= 10

        if self.crashed:
            self.fitness /= 1000

        self.fitness **=4


        


