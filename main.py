
import pygame

from rocket import Rocket
from population import Population

if __name__ == "__main__":
    
    window_width = 1000
    window_height = 700

    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Smart rockets")

    FPS = 180
    clock = pygame.time.Clock()

    count = 0
    frames = 800

    target_x = int(window_width/2)
    target_y = 20

    obstacle_x = 200
    obstacle_y = int(window_height/2)
    obstacle_width = 600
    obstacle_height = 20

  
    rect = pygame.draw.rect(window, (0,0,255), (obstacle_x,obstacle_y,obstacle_width,obstacle_height))



    population = Population(25, frames, window_width/2, window_height, window_width, window_height, 
    target_x, target_y, rect)

  
    count = 0
    population.evaluate(target_x, target_y)
    population.natural_selection()
    population.generate()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_LEFT]:
        #     rocket.rotateLeft()

        # if keys[pygame.K_RIGHT]:
        #     rocket.rotateRight()
        
        # if keys[pygame.K_UP]:
        #     rocket.accelerate()

        if count > frames:
            count = 0
            population.evaluate(target_x, target_y)
            population.natural_selection()
            population.generate()
        else:
            
            count = count+1

        population.run(count)
        if population.checkAlive() == 0:
            count = 0
            population.evaluate(target_x, target_y)
            population.natural_selection()
            population.generate()


        window.fill((0,0,0))
        population.draw(window)

        pygame.draw.circle(window, (0, 255, 0), (target_x, target_y), 20)
        pygame.draw.rect(window, (0,0,255), (obstacle_x,obstacle_y,obstacle_width,obstacle_height))
        pygame.display.update()

    pygame.quit()
        
