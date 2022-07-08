
import pygame
import math
import random
#import time
#import operator
#from nnet import Nnet
from defs import *
from course import Course
from bike import Bike, BikeCollection
from shapely.geometry import LineString



def run_game():

    # start pygame
    pygame.init()

    # initialize game display
    gameDisplay = pygame.display.set_mode((DISPLAY_W,DISPLAY_H))
    pygame.display.set_caption(GAME_NAME)


#    bgImg = pygame.image.load(BG_FILENAME)
#    pipes = PipeCollection(gameDisplay)
#    pipes.create_new_set()
    course = Course(gameDisplay)
    course.import_course()

    bikes = BikeCollection(gameDisplay,course)
#    bike = Bike(gameDisplay,add_pos(course.course_points[1].pos,(0,course.course_width*.1)) )

    label_font = pygame.font.SysFont("arial", DATA_FONT_SIZE)

    clock = pygame.time.Clock()
    dt = 0
    game_time = 0
    num_iterations = 1  

    # establish loop for game  
    running = True
    while running:

        dt = clock.tick(FPS)
        game_time += dt
        gameDisplay.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                running = False

        course.update_game()
        num_alive = bikes.update(course,game_time)

        if num_alive == 0:
            game_time = 0
            bikes.evolve_population(course)
            num_iterations += 1

        update_data_labels(gameDisplay, dt, game_time, num_iterations, num_alive, label_font)
        pygame.display.update()
    
    pygame.display.quit
    pygame.quit()




if __name__== "__main__":
    run_game()
    