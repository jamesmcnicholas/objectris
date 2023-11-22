import pygame
import pygame.freetype
import json
import random
from random import randint

frame_counter = 0
speed = 60
tetromino_colour = ""
height = 40
width = 40
margin = 5
colour = "white"
bag = []
active_position = [[], [], [], []]
screen_width = 1920
screen_height = 1080
offset_mid_x = screen_width/2 - (width*5)
offset_mid_y = screen_height/2 - (height*10)

# --- build the board model --- #
board = []
for row in range (20):
    board.append([])
    for column in range(10):
        board[row].append(0)

pygame.init()
pygame.freetype.init()
GAME_FONT = pygame.freetype.Font("RobotoMono-Bold.ttf", 80)
 
# Set the width and height of the screen [width, height]
size = (screen_width, screen_height)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Tetris")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
# --- background ---
#create the locations of the stars for when we animate the background
star_field_slow = []
star_field_medium = []
star_field_fast = []

for slow_stars in range(50): #birth those plasma balls, baby
    star_loc_x = random.randrange(0, screen_width)
    star_loc_y = random.randrange(0, screen_height)
    star_field_slow.append([star_loc_x, star_loc_y]) #i love your balls

for medium_stars in range(35):
    star_loc_x = random.randrange(0, screen_width)
    star_loc_y = random.randrange(0, screen_height)
    star_field_medium.append([star_loc_x, star_loc_y])

for fast_stars in range(15):
    star_loc_x = random.randrange(0, screen_width)
    star_loc_y = random.randrange(0, screen_height)
    star_field_fast.append([star_loc_x, star_loc_y])

#define some star colours
LIGHTGREY = (192, 192, 192)
DARKGREY = (128, 128, 128)
YELLOW = (224, 224, 224)
                                 


# --- helper methods ---
def generate_bag():
    return random.sample(range(0, 7), 7)

def convert_to_tetromino_letter(number):
    if number == 0:
        return "I"
    if number == 1:
        return "J"
    if number == 2:
        return "L"
    if number == 3:
        return "O"
    if number == 4:
        return "S"
    if number == 5:
        return "T"
    if number == 6:
        return "Z"

def convert_letter_to_colour(letter):
    if letter == "I":
        return "cyan"
    if letter == "J":
        return "blue"
    if letter == "L":
        return "orange"
    if letter == "O":
        return "yellow"
    if letter == "S":
        return "green"
    if letter == "T":
        return "purple"
    if letter == "Z":
        return "red"

def spawn_tetromino():
    global bag
    global active_position
    global tetromino_colour
    if bag == []:
        bag = generate_bag()
    letter = convert_to_tetromino_letter(bag.pop(0))
    tetromino = get_tetromino(letter,0)
    tetromino_colour = letter
    print(letter)
    for cell in tetromino:
        board[cell[1]][cell[0]+3] = tetromino_colour
    for i in range(4):
        active_position[i].append(tetromino[i][1])
        active_position[i].append(tetromino[i][0]+3)

def check_left():
    for i in range(4):
        if active_position[i][1] - 1 < 0:
            return False

def check_right():
    for i in range(4):
        if active_position[i][1] + 1 > 9:
            return False

def check_down():
    for i in range(4):
        if active_position[i][0] + 1 > 19:
            return False

def move_left():
    global board
    if check_left() == False:
        return
    else:
        board = [[0 for x in range(10)] for y in range(20)]
        for i in range(4):
            active_position[i][1] = active_position[i][1] - 1
        for cell in active_position:
            board[cell[0]][cell[1]] = tetromino_colour
        print(active_position)
    
def move_right():
    global board
    if check_right() == False:
        return
    else:
        board = [[0 for x in range(10)] for y in range(20)]
        for i in range(4):
            active_position[i][1] = active_position[i][1] + 1
        for cell in active_position:
            board[cell[0]][cell[1]] = tetromino_colour
    

def move_down():
    global board
    if check_down() == False:
        return
    else:
        board = [[0 for x in range(10)] for y in range(20)]
        for i in range(4):
            active_position[i][0] = active_position[i][0] + 1
        for cell in active_position:
            board[cell[0]][cell[1]] = tetromino_colour
    print(active_position)


def fall():
    global board
    global board
    if check_down() == False:
        return
    else:
        board = [[0 for x in range(10)] for y in range(20)]
        for i in range(4):
            active_position[i][0] = active_position[i][0] + 1
        for cell in active_position:
            board[cell[0]][cell[1]] = tetromino_colour

# --- load tetrominoes --- 
with open('tetrominoes.json') as jsonfile:
    tetrominoes = json.load(jsonfile)
    def get_tetromino(type, rotation):
        return tetrominoes.get(type)[rotation]

spawn_tetromino()

bg = pygame.image.load("space.jpg")
# play_area = pygame.Surface((1920,1080))
# play_area.fill((255,255,255,1))
# play_area = pygame.draw.rect(screen, (255,255,255), (50, 50, 50, 50), 1)
# play_area = pygame.transform.gaussian_blur(play_area, 20)

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                move_left()
            if event.key == pygame.K_LEFT:
                move_left()
            if event.key == pygame.K_d:
                move_right()
            if event.key == pygame.K_RIGHT:
                move_right()
            if event.key == pygame.K_s:
                move_down()
            if event.key == pygame.K_DOWN:
                move_down()
 
    # --- Game logic should go here

    # gravity for active block
    frame_counter += 1
    if frame_counter % speed == 0:
        fall()
 
    # --- Screen-clearing code goes here
 
    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.

    screen.blit(bg, (0,0))
    

    # Draw Title
    GAME_FONT.render_to(screen, (100, 50), "TETRIS", (255, 255, 255))


    # --- background animation ---
    for star in star_field_slow:
        star[1] += 1
        if star[1] > screen_height:
            star[0] = random.randrange(0, screen_width)
            star[1] = random.randrange(-20, -5)
        pygame.draw.circle(screen, DARKGREY, star, 3)

    for star in star_field_medium:
        star[1] += 4
        if star[1] > screen_height:
            star[0] = random.randrange(0, screen_width)
            star[1] = random.randrange(-20, -5)
        pygame.draw.circle(screen, LIGHTGREY, star, 2)

    for star in star_field_fast:
        star[1] += 8
        if star[1] > screen_height:
            star[0] = random.randrange(0, screen_width)
            star[1] = random.randrange(-20, -5)
        pygame.draw.circle(screen, YELLOW, star, 1)

    # --- Drawing code should go here

    

    # draw grid
    offset_x = offset_mid_x
    offset_y = offset_mid_y
    for row in range(20):
        offset_y += margin
        for column in range(10):

            if(board[row][column] != 0):
                colour = convert_letter_to_colour(tetromino_colour)
                filled = 0
            else:
                colour = "white"
                filled = 1

            offset_x += margin
            pygame.draw.rect(screen, colour, (offset_x, offset_y, width, width), filled)
            offset_x += width
        offset_x = offset_mid_x
        offset_y += height


    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)

 
# Close the window and quit.
pygame.quit()
