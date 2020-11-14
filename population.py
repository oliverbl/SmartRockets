from rocket import Rocket
import random
import functools

class Population(object):
    def __init__(self, number, frames, pos_x, pos_y, width, height, target_x, target_y, obstacle):
        self.rockets = []

        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.frames = frames
        self.target_x = target_x
        self.target_y = target_y
        self.obstacle = obstacle

        for _ in range(number):
            rocket = Rocket(pos_x, pos_y, frames, width, height, target_x, target_y, obstacle)
            self.rockets.append(rocket)
            # rocket.random()
        self.fittest = self.rockets[0]
        self._mutation_rate = 0.01
    
    def run(self, count):
        
        for r in self.rockets:
            r.update(count)

    def draw(self, window):
        for r in self.rockets:
            r.draw(window)

    def checkAlive(self):
        count = 0
        for r in self.rockets:
            if not r.offscreen():
                count = count + 1
        return count

    def evaluate(self, target_x, target_y):
        for r in self.rockets:
            r.calcFitness()
            if r.fitness == 0:
                return True
        return False

    def natural_selection(self):
        self.fittest = max(self.rockets, key=lambda e: e.fitness)
        print("fittest: {}".format(self.fittest.fitness))


    def select(self):
        sum = functools.reduce(lambda sum, e: sum + e.fitness, self.rockets, 0)
        
        weights = []
        for e in self.rockets:
            weights.append(e.fitness / sum)

        r = random.uniform(0, 1)
        i = 0
        while r > 0:
            r = r - weights[i]
            i += 1
        
        i -= 1
        return self.rockets[i]

    def generate(self):
        newPopulation = []

        for _ in range(len(self.rockets)):
            a = self.select()
            b = self.select()
            child = a.dna.crossover(b.dna)
            child.mutate(self._mutation_rate)

            newPopulation.append(Rocket(self.pos_x, self.pos_y, self.frames, self.width, self.height, self.target_x, self.target_y, self.obstacle, child))
        self.rockets = newPopulation