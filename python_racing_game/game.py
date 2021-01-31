# Author: Damian Hruban
# UCO: 451864
# Title: Get out of my way
# Desription: Trabant racing game

import sys
import os
import pygame
import random
from time import sleep

pygame.init()

# SETS NAME OF WINDOW
pygame.display.set_caption("GET OUT OF MY WAY")

# DEFINES CONSTANS
WIDTH = 1050
HEIGHT = 738
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

base_path = os.path.dirname(__file__)
enemy_y = random.randrange(100, HEIGHT - 100)
time_machine = pygame.time.Clock()

# LOADS ALL IMAGES FOR THE GAME
def load_img(img_name):
    abs_path = os.path.join(base_path, img_name) # generates absolute path (relative doesnt work)
    loaded_img = pygame.image.load(abs_path)
    return loaded_img

road = load_img("images//roads//main_road.png")       # pokud vraci errory s sRGB a CCT - online PNG CRUSH CONVERTER
trabant_img = load_img("images//trabant_s.png")
trabant_len = trabant_img.get_width()
trabant_height = trabant_img.get_height()
enemy_1 = load_img("images//enemies//bus_l.png")

enemy_2 = load_img("images//enemies//pickup_m.png") 
enemy_3 = load_img("images//enemies//truck_m.png")
enemy_4 = load_img("images//enemies//lorry_b.png")
blast_1 = load_img("images//effects//blast.png").convert_alpha()
blast_1_w = blast_1.get_width()
blast_1_h = blast_1.get_height()

# DEFINES TEXT IN THE GAME
font_1 = pygame.font.SysFont("None", 40)

def render_moving_road(x, road_speed):
    SCREEN.blit(road, (x, 0))
    SCREEN.blit(road, (x + road.get_width(), 0))  # renders road for the second time right behind the first one
    x -= road_speed # moves background road to the left with defined speed
    if x < (-1 * (road.get_width())): # if first image gets out of the window - returns to initial position
        x = 0
    return x

def place_car(car_img, coord_x, coord_y):
    SCREEN.blit(car_img, (coord_x, coord_y))

def sending_cars(x, y, enemy):
    chosen_car = enemy_1
    # DECIDES WHAT CAR TO SEND
    if enemy % 4 == 0: # for 3 types of enemy cars
        chosen_car = enemy_1
    elif enemy % 4 == 1:
        chosen_car = enemy_2
    elif enemy % 4 == 2:
        chosen_car = enemy_3
    elif enemy % 4 == 3:
        chosen_car = enemy_4        
    place_car(chosen_car, x, y) # renders chosen car
    return chosen_car

def score_rendering(score_count, cm_count):
    score_text = font_1.render("Meters: " + str(score_count), 1, (0,0,0))
    SCREEN.blit(score_text, (50, 30))
    if cm_count % 20 != 0:  
        return 0
    return 1

# COMPARE AND SAVE NEW HIGHSCORE
def compare_scores(base_path, score_count, new_record):
    score_f_path = os.path.join(base_path, 'score.txt')
    with open(score_f_path, "r") as f:
        high_score = f.readline()
        if score_count > int(high_score):
            new_record = True
            with open(score_f_path, "w") as f:
                f.write(str(score_count))
    return new_record

def crash_alert(score_count, new_record):

    txt_list = []
    if new_record:
        high_score_txt = font_1.render("CONGRATS, NEW RECORD!", 1, (100,100,100))
        txt_list.append(high_score_txt)

    crash_text = font_1.render("You crashed after " + str(score_count) + " meters", 1, (0,0,0))
    again_text = font_1.render("Start again?       Press S", 1, (100,100,100))
    quit_text = font_1.render( "Quit?                  Press Q", 1, (100,100,100))    
    txt_list.extend((crash_text, again_text, quit_text))
    y = (HEIGHT/2) - 150
    # SHOWS SAVED TEXTS FROM txt_list
    for line in txt_list:        
        SCREEN.blit(line, (WIDTH//3, y))
        y += 50 # new line
        

def game_cycle():
    """MAIN GAME FCN - loops until exit_game is True
    """
    crashed = False
    exit_game = False
    new_record = False
    x_change = 0
    y_change = 0
    x_coord = WIDTH/2
    y_coord = HEIGHT/2
    enemy_speed = 3
    enemy_number = 0
    enemy_x = -300

    road_speed = 2
    road_x_coord = 0

    cm_count = 0
    score_count = 0
        
    while not exit_game:
        while crashed:
                       
            SCREEN.blit(blast_1, (x_coord - (blast_1_w // 2) , y_coord - (blast_1_h // 2))) # renders bang image
            pygame.display.flip()
            pygame.time.wait(1000)
            blast_1.set_alpha(0) # makes bang image invisible

            # CHECK FOR HIGH SCORE AND WRITES GAME RESULT
            SCREEN.fill((255,255,255))
            pygame.display.update()
            crash_alert(score_count, compare_scores(base_path, score_count, new_record))
            pygame.display.update()

            # LOGIC FOR GAME MENU
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        exit_game = True
                        crashed = False
                        new_record = False
                        sys.exit()
                    if event.key == pygame.K_s:
                        blast_1.set_alpha(255)
                        new_record = False
                        game_cycle()
        # LOGIC FOR EXITING GAME
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:
                pygame.quit()
                exit_game = True
                sys.exit()

            # LOGIC FOR CAR MOVEMENT - PRESSING ARROWS
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_LEFT:
                    if x_coord > 20:            # left limit, vytvorit mimo funkci check bounderies (somerimes car jumps over limit anyway-- while pressing combinations of arrows(diagonal move))
                        x_change = -5   
                    else:
                        x_change = 0
                if event.key == pygame.K_RIGHT:
                    if x_coord < 890:           # right limit
                        x_change = 5   
                    else:
                        x_change = 0
                if event.key == pygame.K_UP:
                    if y_coord > 30:            # up limit
                        y_change = -5
                    else:
                        y_change = 0                    
                if event.key == pygame.K_DOWN:
                    if y_coord < 650:           # down limit
                        y_change = 5
                    else:
                        y_change = 0
            if event.type == pygame.KEYUP:    # LOGIC FOR RELEASING KEYS
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    y_change = 0     

        # SETS ROAD AS BACKGROUND
        road_x_coord = render_moving_road(road_x_coord, road_speed)

        x_coord += x_change
        y_coord += y_change

        # ENEMY CARS MOVEMENT AND INCREASING SPEED    
        global enemy_y
        chosen_enemy = sending_cars(enemy_x, enemy_y, enemy_number)
        enemy_width = chosen_enemy.get_width()
        enemy_height = chosen_enemy.get_height()        

        if enemy_x > 1300:
            enemy_x = -300
            enemy_y = random.randrange(100, HEIGHT - 100)
            enemy_number += 1
            enemy_speed += 0.5 # after each enemy car pass the speed increases
        enemy_x += enemy_speed     

        # TRABANT PLACEMENT AND DRIVING RANGE
        place_car(trabant_img, x_coord, y_coord)
        margin = 70
        if y_coord > HEIGHT - margin:
            y_coord = HEIGHT - margin
        if y_coord < margin // 2:
            y_coord = margin // 2
        if x_coord > WIDTH - trabant_len - margin // 2:
            x_coord = WIDTH - trabant_len - margin // 2
        if x_coord < margin // 2:
            x_coord = margin // 2
            
        # COLLISION CHECKER
        tolerance_pix = 40
        trabant_rect = pygame.Rect(x_coord + tolerance_pix, y_coord + tolerance_pix, trabant_len - tolerance_pix, trabant_height - tolerance_pix)
        enemy_rect = pygame.Rect(enemy_x + tolerance_pix, enemy_y + tolerance_pix, enemy_width - tolerance_pix,  enemy_height - tolerance_pix)
        if trabant_rect.colliderect(enemy_rect):
            crashed = True   

        # COUNTS DISTANCE (SCORE) AND RENDERS IT
        score_count += score_rendering(score_count, cm_count)
        cm_count += 1        

        # SHOWS CHANGES AFTER ONE LOOP
        pygame.display.update()
        time_machine.tick(120)    # SLOWING DOWN SPEED OF THE CAR - FPS
# CALLING MAIN GAME FCN
game_cycle()