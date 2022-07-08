import math
import operator
from shapely.geometry import LineString, Point

def update_label(data, title, font, x, y, gameDisplay):
    label = font.render('{} {}'.format(title, data), 1, DATA_FONT_COLOR)
    gameDisplay.blit(label, (x, y))
    return y

def update_data_labels(gameDisplay, dt, game_time, num_iterations, num_alive, font):
    y_pos = 10
    gap = 20
    x_pos = 10
    y_pos = update_label(round(1000/dt,2), 'FPS', font, x_pos, y_pos + gap, gameDisplay)
    y_pos = update_label(round(game_time/1000,2),'Game time', font, x_pos, y_pos + gap, gameDisplay)
    y_pos = update_label(num_iterations,'Iteration', font, x_pos, y_pos + gap, gameDisplay)
    y_pos = update_label(num_alive,'Alive', font, x_pos, y_pos + gap, gameDisplay)
    
# move based on radians and distance, indexed to 0,0
def new_pos(rads, offset):
    x = math.cos(rads) * offset
    y = math.sin(rads) * offset
    return (x, y)

# add two positions together
def add_pos(pos1,pos2):
    return tuple(map(operator.add, pos1, pos2)) 

#calc hypot
def distance_between(pos1,pos2):
    return math.hypot(pos1[0]-pos2[0], pos1[1]-pos2[1])


def lines_intersect_bool(line1_start,line1_end,line2_start,line2_end):
    line = LineString([(line1_start),(line1_end)])
    other = LineString([(line2_start),(line2_end)]) 
    
    return line.intersects(other)


def lines_intersect_pos(line1_start,line1_end,line2_start,line2_end):
    line = LineString([(line1_start),(line1_end)])
    other = LineString([(line2_start),(line2_end)]) 
    
    int_pt = line.intersection(other)
    try: 
        x , y = ( int_pt.coords.xy)
        result = (list(x)[0],list(y)[0])
    except: result=None
    return result

def lines_intersect_pos2(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       result = None
    else:
        d = (det(*line1), det(*line2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        result = x, y
    return result



GAME_NAME ='Leadout'
DISPLAY_W=1000
DISPLAY_H=800

DATA_FONT_SIZE=20
DATA_FONT_COLOR = (255, 255, 255)

FPS=30

COURSE_COLOR = (255, 255, 255)

BLACK = (0, 0, 0)

BIKE_STARTING_OFFSET_X = 10
BIKE_COLOR = (0, 0, 255)
BIKE_HIGHLIGHT = (255, 255, 255)
BIKE_WIDTH = 6
BIKE_HEADING_WIDTH = 2
BIKE_ACCELERATION = .05
BIKE_TURN_INCREMENT = .05
BIKE_DECELERATION = .05
REQUIRED_PROGRESS = 8000

GENERATION_SIZE = 10
MUTATION_WEIGHT_MODIFY_CHANCE = 0.2 # how much to change neural net weights
MUTATION_ARRAY_MIX_PERC = 0.5
MUTATION_CUT_OFF = 0.3
MUTATION_BAD_TO_KEEP = 0.1
MUTATION_MODIFY_CHANCE_LIMIT = 0.8 # likelihood that offspring modifies weight

NNET_INPUTS = 7
NNET_HIDDEN = 4
NNET_OUTPUTS = 2
COMMAND_CHANCE_FORWARD = 0.4 #.35
COMMAND_CHANCE_SLOW = 0.4 #.25
COMMAND_CHANCE_TURN_RIGHT = 0.45 #.45
COMMAND_CHANCE_TURN_LEFT = 0.55 #.55

COURSE_FILENAME = 'course_vertices.csv'
COURSE_WIDTH=80

VISION_LINE_LENGTH_MAX = DISPLAY_W*2
VISION_WIDTH = 1
VISION_COLOR = (0,255,0)