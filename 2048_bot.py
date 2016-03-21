from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
import time

################################################

driver = webdriver.Firefox()
driver.maximize_window()
driver.get('http://gabrielecirulli.github.io/2048')
time.sleep(2)
body_tag = driver.find_element_by_tag_name('body')
body_tag.send_keys(Keys.DOWN)
body_tag.send_keys(Keys.DOWN)
body_tag.send_keys(Keys.DOWN)
body_tag.send_keys(Keys.DOWN)

###############################################

def find_game_container(driver):
    tile_container = driver.find_element_by_class_name('tile-container')
    return tile_container

################################################

def parse_classname(s):
    '''
    ex: s = 'tile tile-4 tile-position-1-2 tile-new'
    ou  'tile tile-4 tile-position-1-4'
      'tile tile-4 tile-position-3-4 tile-merged'
      
    Returns: ((row, col), value, flag)
    '''
    flag = None
    fields = s.replace('-', ' ').split(' ')
    # ex: [u'tile', u'tile', u'4', u'tile', u'position', u'1', u'2', u'tile', u'new']
    value = int(fields[2])
    row = int(fields[6])
    col = int(fields[5])
    
    if len(fields) == 9:
        flag = fields[8]
    
    return ((row, col), value, flag)

##################################################

def get_grid(tile_container):
    
    tiles = tile_container.find_elements_by_class_name('tile')
    # information can be retrieved from tile class names:
    tile_classes = [t.get_attribute('class') for t in tiles]
    
    # a list of tiles (row, col), value, flag)
    tiles_data = [parse_classname(s) for s in tile_classes]
    
    # Build the grid
    grid = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]]

    for ((row, col), value, flag) in tiles_data:
        if flag == 'merged':
            continue # discard, use the "underlying tiles" addition instead
        grid[row-1][col-1] += value
    
    return grid

######################################################

def print_grid(grid):
    for r in grid:
        r = ['{:4d}'.format(c) for c in r]
        print(' '.join(r))

######################################################

def rotate_right(b):
    copy = [[0 for x in range(4)]for y in range(4)]
    for i in range(4):
        for j in range(4):
            copy[i][j] = b[4-j-1][i]
    b = [[copy[x][y] for y in range(4)]for x in range(4)]

######################################################

def rotate_left(b):
    copy = [[0 for x in range(4)]for y in range(4)]
    for i in range(4):
        for j in range(4):
            copy[4-j-1][i] = b[i][j]
    b = [[copy[x][y] for y in range(4)]for x in range(4)]

######################################################

def get_points(direction,b):
    c = [[b[i][j] for j in range(4)]for i in range(4)]
    points = 0

    if(direction == 'up'):
        rotate_left(c)
    elif(direction == 'right'):
        rotate_left(c)
        rotate_left(c)
    elif(direction == 'down'):
        rotate_right(c)

    for i in range(4):
        last_merge_position = 0
        for j in range(1,4):
            if(c[i][j] == 0):
                continue #skipping zeroes
            previous_position = j-1

            while(previous_position > last_merge_position and c[i][previous_position]==0):
                previous_position -= 1

            if(previous_position == j):
                pass #we can't move at all
            elif(c[i][previous_position] == 0):
                #move to emplty place
                c[i][previous_position] = c[i][j]
                c[i][j] = 0
            elif(c[i][previous_position] == c[i][j]):
                #merge with matching value
                c[i][previous_position] *= 2
                c[i][j] = 0
                points += c[i][previous_position]
                last_merge_position = previous_position + 1
            elif(c[i][previous_position] != c[i][j] and (previous_position + 1) != j):
                c[i][previous_position+1] = c[i][j]
                c[i][j] = 0

    return points

######################################################
tile_container = find_game_container(driver)
grid = get_grid(tile_container)

while(True):
    maximum = 0
    temp = get_points('right',grid)
    move = -1
    scores = []
    scores.append([0,temp])
    if(temp > maximum):
        move = 0
        maximum = temp
    temp = get_points('down',grid)
    scores.append([1,temp])
    if(temp > maximum):
        move = 1
        maximum = temp
    temp = get_points('up',grid)
    scores.append([2,temp])
    if(temp > maximum):
        move = 2
        maximum = temp

    for k in range(3):
        for l in range(0,k):
            if(scores[k][1] > scores[l][1]):
                scores[k][1],scores[l][1] = scores[l][1],scores[k][1]
    
    if(move == 0):
        tile_container.send_keys(Keys.DOWN)
    elif(move == 1):
        tile_container.send_keys(Keys.RIGHT)
    elif(move == 2):
        tile_container.send_keys(Keys.UP)
    else:
        x = scores[1][0]
        if(x==0):
            tile_container.send_keys(Keys.RIGHT)
        elif(x==1):
            tile_container.send_keys(Keys.DOWN)
        else:
            tile_container.send_keys(Keys.UP)

        time.sleep(0.2)
        tile_container = find_game_container(driver)
        grid_copy = get_grid(tile_container)

        if(grid_copy == grid):
            x = scores[2][0]
            if(x==0):
                tile_container.send_keys(Keys.RIGHT)
            elif(x==1):
                tile_container.send_keys(Keys.DOWN)
            else:
                tile_container.send_keys(Keys.UP)
            
    time.sleep(0.2)

    tile_container = find_game_container(driver)
    grid_copy = get_grid(tile_container)
    if(grid_copy == grid):
        break
    grid = get_grid(tile_container)
