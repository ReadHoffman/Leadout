import csv
import pygame
from defs import *
from course import Course, Course_Point
import math


def run_course_creator():

    pygame.init()
    gameDisplay = pygame.display.set_mode((DISPLAY_W,DISPLAY_H))
    pygame.display.set_caption('CRIT RACE COURSE CREATOR')

    running = True

    label_font = pygame.font.SysFont("arial", DATA_FONT_SIZE)

    clock = pygame.time.Clock()
#    dt = 0
#    game_time = 0
#    num_iterations = 1    
    
    course = Course(gameDisplay)
    
    # make cursor visible
    pygame.mouse.set_visible(True)
    pygame.mouse.set_cursor(*pygame.cursors.broken_x)

    while running:

#        dt = clock.tick(FPS)
#        game_time += dt
        gameDisplay.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                running = False
        click = (pygame.mouse.get_pressed() == (1, 0, 0) )
        mouse_pos = pygame.mouse.get_pos()

#        pipes.update(dt)
        course.update_course_creator(click,mouse_pos)
#        draw_created_course()
#        num_alive = 0 #birds.update(dt, pipes.pipes)

#        if num_alive == 0:
#            pipes.create_new_set()
#            game_time = 0
#            birds.evolve_population()
#            num_iterations += 1

#        update_data_labels(gameDisplay, dt, game_time, num_iterations, num_alive, label_font)
        pygame.display.flip()
        
        # define list of places
    
#    with open('course_vertices.txt', 'w') as filehandle:
#        for listitem in course.course_points:
#            filehandle.write('%s\n' % listitem)
    
    
    with open(COURSE_FILENAME, 'w', newline='') as csvfile:
        fieldnames = ['i','x', 'y']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
        writer.writeheader()
        
        for i, course_point in enumerate(course.course_points):
            writer.writerow({'i':i,'x': course_point.pos[0], 'y': course_point.pos[1]})

    
#    
#    with open('course_vertices.txt', 'wb') as f:
#        course_point_x
#        course_point_y
#        for course_point in course.course_points:
#        csv.writer(f, delimiter=',').writerows(course.course_points)
    
    
    pygame.display.quit
    pygame.quit()




if __name__== "__main__":
    run_course_creator()