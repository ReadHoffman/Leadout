import pygame
from defs import *
import math
import operator
import csv
from shapely.geometry import LineString
from itertools import cycle

class Course_Point:
    def __init__(self,pos):
        self.pos = pos
        self.i = 0
        self.diameter = COURSE_WIDTH
        self.radius = self.diameter/2
        self.radians_lag_lead = 0
        self.radians_lag_lead_midpoint = 0
        self.radians_lag_lead_inverse = 0
        self.radians_lag_lead_midpoint_inverse = 0
        self.radians_lag_lead2 = 0
        self.end_point = False
        self.distance_to_point_lag = 0
        self.vector_to_point_lag = 0
        self.radians_to_point_lag = 0
        self.distance_to_point_lead = 0
        self.vector_to_point_lead = 0
        self.radians_to_point_lead = 0
        self.distance_to_point_lead2 = 0
        self.vector_to_point_lead2 = 0
        self.radians_to_point_lead2 = 0
        self.pos_left = 0
        self.pos_right = 0

class Course:
    def __init__(self,gameDisplay):
        self.gameDisplay = gameDisplay
        self.outer_num = 8
        self.inner_num = 8
        self.course_width = COURSE_WIDTH
        self.course_points = []
        self.outer_verticies = [] #[(DISPLAY_W*1/10,DISPLAY_H*1/10),(DISPLAY_W*9/10,DISPLAY_H*1/10),(DISPLAY_W*9/10,DISPLAY_H*9/10),(DISPLAY_W*1/10,DISPLAY_H*9/10),(DISPLAY_W*1/10,DISPLAY_H*1/10)]
        self.inner_verticies = [] #[(DISPLAY_W*3/10,DISPLAY_H*3/10),(DISPLAY_W*7/10,DISPLAY_H*3/10),(DISPLAY_W*7/10,DISPLAY_H*7/10),(DISPLAY_W*3/10,DISPLAY_H*7/10),(DISPLAY_W*3/10,DISPLAY_H*3/10)]
        self.progress_lines = []
    
    def import_course(self):
        with open(COURSE_FILENAME,newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            loaded_points = []
            for row in reader:
#                data = (int(row["index"]),int(row["x"]), int(row["y"]))
                point = Course_Point( ( int(row["x"]),int(row["y"]) )  )
                loaded_points.append(point)
            self.course_points = loaded_points
            self.reset_course_point_index()
        self.compute_course_point_relationships()
        self.create_boundaries()
    
    def create_course_points(self,click,mouse_pos):
        if click==True:
            new_point_check = [distance_between(mouse_pos,course_point.pos) > self.course_width/2 for course_point in self.course_points ]
            if len(new_point_check)==0 or all(new_point_check):
                point = Course_Point(mouse_pos)
                self.course_points.append(point)
                
                #on first click, porduce starting area with space for bikes ahead of and behind start line
                if len(self.course_points)==1:
                    point_lead = Course_Point(add_pos(self.course_points[0].pos,(self.course_width*2,0)))
                    self.course_points.append(point_lead)
                    point_lag = Course_Point(add_pos(self.course_points[0].pos,(-self.course_width*2,0)))
                    self.course_points.insert(0,point_lag)
                
                    
    def reset_course_point_index(self):
        for i, point in enumerate(self.course_points):
            point.i = i
    
    def compute_course_point_relationships(self):
        ## the following steps will allow our formula to reference surrounding points
        ## and update data for that point accordingly
        point_list = self.course_points
        point_list_len = len(point_list)
        
#        #add last point to front of list
#        point_list.insert(0,point_list[point_list_len-1])
#        point_list.insert(0,point_list[point_list_len-1])
#        
#        #take oringinal starting point 1 an 2 and add it to the end
#        point_list.append(point_list[1])
#        point_list.append(point_list[2])
        
        for i in range(point_list_len):
            i_lag = i-1
            i_lead = i+1
            i_lead2 = i+2
            if i ==1 :
                i_lag = point_list_len-1
#                i_lead = i+1
#                i_lead2 = i+2
            if i ==point_list_len-2 :
#                i_lag = i-1
#                i_lead = i+1
                i_lead2 = 0
            if i ==point_list_len-1 :
#                i_lag = i-1
                i_lead = 0
                i_lead2 = 1
                
            point_lag = point_list[i_lag]
            point_main = point_list[i]
            point_lead = point_list[i_lead]
            point_lead2 = point_list[i_lead2]
            
            point_main.distance_to_point_lag = distance_between(point_lag.pos,point_main.pos)
            point_main.distance_to_point_lead = distance_between(point_main.pos,point_lead.pos)
            point_main.distance_to_point_lead2 = distance_between(point_main.pos,point_lead2.pos)
            
            point_main.vector_to_point_lag = tuple(map(operator.sub,point_lag.pos,point_main.pos))
            point_main.vector_to_point_lead = tuple(map(operator.sub,point_lead.pos,point_main.pos))
            point_main.vector_to_point_lead2 = tuple(map(operator.sub,point_lead2.pos,point_main.pos))
            
            point_main.radians_to_point_lag = math.atan2(*point_main.vector_to_point_lag)-math.pi/2
            point_main.radians_to_point_lead = math.atan2(*point_main.vector_to_point_lead)-math.pi/2
            point_main.radians_to_point_lead2 = math.atan2(*point_main.vector_to_point_lead2)-math.pi/2
            
            point_main.radians_lag_lead = point_main.radians_to_point_lag-point_main.radians_to_point_lead
            point_main.radians_lag_lead2 = point_main.radians_to_point_lag-point_main.radians_to_point_lead2
            angles_list_lag_lead = [point_main.radians_to_point_lag,point_main.radians_to_point_lead]
            point_main.radians_lag_lead_midpoint = sum(angles_list_lag_lead)/len(angles_list_lag_lead)
            point_main.radians_lag_lead_midpoint_inverse = point_main.radians_lag_lead_midpoint+math.pi
    
    def create_boundaries(self):   
        for point in self.course_points:
            
            #must multiply by -1 since pygame y axis flipped
            inner = add_pos(new_pos(point.radians_lag_lead_midpoint*-1, point.radius),point.pos ) 
            outer = add_pos(new_pos(point.radians_lag_lead_midpoint_inverse*-1, point.radius),point.pos )
            
            self.outer_verticies.append( outer )
            self.inner_verticies.append( inner )
        
        #clean up intersections
        course_points_len = len(self.course_points)
        for i in range(course_points_len*2-1): 
            if i>course_points_len-1: i = i-course_points_len-1
            outer_point = self.outer_verticies[i]   
            inner_point = self.inner_verticies[i]
            
            if i== 0: i_lag=len(self.course_points)-1
            else: i_lag = i-1
            if lines_intersect_bool(self.course_points[i].pos,self.course_points[i_lag].pos,self.inner_verticies[i],self.inner_verticies[i_lag]):
                self.outer_verticies[i] = inner_point
                self.inner_verticies[i] = outer_point
                
        self.progress_lines = [(self.inner_verticies[i] ,self.outer_verticies[i]) for i in range(len(self.inner_verticies))]                
            
            
    def draw_created_course(self):
        [pygame.draw.circle(self.gameDisplay, (255, 255, 255), course_point.pos,int(course_point.radius) ) for course_point in self.course_points]
        
    def update_course_creator(self,click,mouse_pos):
        self.create_course_points(click,mouse_pos)
        self.draw_created_course()

    def draw_game(self):
        pygame.draw.lines(self.gameDisplay, (100, 100, 100), True, [x.pos for x in self.course_points])
        pygame.draw.lines(self.gameDisplay, (255, 255, 255), True, self.outer_verticies)
        pygame.draw.lines(self.gameDisplay, (255, 255, 255), True, self.inner_verticies)
        [pygame.draw.lines(self.gameDisplay, (50, 50, 50), True, progress_line) for progress_line in self.progress_lines]
        
    def update_game(self):
        self.draw_game()
