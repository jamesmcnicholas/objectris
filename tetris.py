import pygame
import pygame.freetype
import json
import random
from random import randint
import time

# --- Gameplay vars ---
frame_counter = 0
speed = 60
tetromino_colour = ""
height = 40
width = 40
margin = 5
colour = "white"
bag = []
touch_bottom = False
lock_in_timer = 0
move_count = 0
active_position = [[], [], [], []]
screen_width = 1920
screen_height = 1080
offset_mid_x = screen_width/2 - (width*5)
offset_mid_y = screen_height/2 - (height*13)
board_width = 10
board_height = 23
saved_piece_type = ""
current_piece_type = ""
place_holder = ""
saved_piece_pane_offset_x = 500
saved_piece_pane_offset_y = offset_mid_y * 8
has_swapped_piece = False
current_piece_orientation = 0

# --- build the board model --- #
board = []
for row in range (board_height):
    board.append([])
    for column in range(board_width):
        board[row].append(0)


pygame.init()
pygame.freetype.init()
GAME_FONT = pygame.freetype.Font("RobotoMono-Bold.ttf", 80)
SECONDARY_FONT = pygame.freetype.Font("RobotoMono-Bold.ttf", 30)
 
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
    # if third row is clear
    if board[2] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
        spawn(1,False)
    # else if second row is clear
    elif board[1] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
        spawn(0,False)


def spawn_saved_piece():
        # if third row is clear
    if board[2] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
        spawn(1,True)
    # else if second row is clear
    elif board[1] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
        spawn(0,True)


def spawn(row_offset,is_saved_piece):
    global bag
    global active_position
    global tetromino_colour
    global current_piece_type
    global has_swapped_piece
    global current_piece_orientation

    active_position = [[],[],[],[]]
    if is_saved_piece:
        letter = saved_piece_type
    else:
        has_swapped_piece = False
        if bag == []:
            bag = generate_bag()
        letter = convert_to_tetromino_letter(bag.pop(0))
    tetromino = get_tetromino(letter,0)
    tetromino_colour = letter
    for cell in tetromino:
        board[cell[1]+row_offset][cell[0]+3] = tetromino_colour
    for i in range(4):
        active_position[i].append(tetromino[i][1]+row_offset)
        active_position[i].append(tetromino[i][0]+3)
    current_piece_type = letter
    current_piece_orientation = 0


def save_symbol():
    global saved_piece_type
    global current_piece_type
    global place_holder
    global has_swapped_piece
    if has_swapped_piece is False:
        if saved_piece_type == "":
            saved_piece_type = current_piece_type
            for i in range(4):
                board[active_position[i][0]][active_position[i][1]] = 0
            spawn_tetromino()
        else:
            place_holder = current_piece_type
            for i in range(4):
                board[active_position[i][0]][active_position[i][1]] = 0
            spawn_saved_piece()
            saved_piece_type = place_holder
            has_swapped_piece = True


# --- scan for movement ---
def check_left():
    for i in range(4):
        if active_position[i][1] - 1 < 0:
            return False
    for j in range(4):
        pos = active_position[j]
        # ensure we're not checking this piece's squares
        if [pos[0],pos[1]-1] not in active_position:
            if board[pos[0]][pos[1]-1] != 0:
                touch_bottom = True
                return False

def check_right():
    for i in range(4):
        if active_position[i][1] + 1 > 9:
            return False
    for j in range(4):
        pos = active_position[j]
        # ensure we're not checking this piece's squares
        if [pos[0],pos[1]+1] not in active_position:
            if board[pos[0]][pos[1]+1] != 0:
                touch_bottom = True
                return False

def check_down():
    global touch_bottom
    global board

    # --- check for bottom of the board ---
    for i in range(4):
        pos = active_position[i]
        if pos[0] + 1 > board_height - 2:
            touch_bottom = True
        else:
            touch_bottom = False
        if pos[0] + 1 > board_height - 1:
            return False

    # --- check for pieces below this piece ---
    for j in range(4):
        pos = active_position[j]
        # ensure we're not checking this piece's squares
        if [pos[0]+1,pos[1]] not in active_position:
            if board[pos[0] + 1][pos[1]] != 0:
                touch_bottom = True
                return False

def check_death():
    if board[1] != [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
        pygame.quit()

def get_full_lines():
    global board
    list_full_lines = []
    for i in range(board_height):
        if not 0 in board[i]:
            list_full_lines.append(i)
    return list_full_lines

# Shift down lines above the cleared line
def clear_lines(full_lines):
    global board
    global board_height
    global board_width
    # For each full line, starting with the lowest
    for line in full_lines:
        # create an empty buffer
        buffer = [0] * board_width
        # loop through every line starting with the bottom full line, going up
        # e.g. line 17 is full, loop 17,16,15....1,0
        for i in range(line,0,-1):
            print("Setting index: ", i, "to index ", i-1)
            # set buffer to the above line
            buffer = board[i-1]
            # set this line to the buffer
            board[i] = buffer
        # Clear the top line
        board[0] = [0] * board_width

# --- move active block ---
def move_left():
    global board
    global lock_in_timer
    global move_count
    global touch_bottom
    if check_left() == False:
        return
    else:
        if touch_bottom is True:
            move_count += 1
        if move_count < 14:
            lock_in_timer = 0
        for cell in active_position:
            board[cell[0]][cell[1]] = 0
        for i in range(4):
            active_position[i][1] = active_position[i][1] - 1
        for cell in active_position:
            board[cell[0]][cell[1]] = tetromino_colour


def move_right():
    global board
    global lock_in_timer
    global move_count
    global touch_bottom
    if check_right() == False:
        return
    else:
        if touch_bottom is True:
            move_count += 1
        if move_count < 14:
            lock_in_timer = 0
        for cell in active_position:
            board[cell[0]][cell[1]] = 0
        for i in range(4):
            active_position[i][1] = active_position[i][1] + 1
        for cell in active_position:
            board[cell[0]][cell[1]] = tetromino_colour


def move_down():
    global board
    if check_down() == False:
        return
    else:
        for cell in active_position:
            board[cell[0]][cell[1]] = 0
        for i in range(4):
            active_position[i][0] = active_position[i][0] + 1
        for cell in active_position:
            board[cell[0]][cell[1]] = tetromino_colour

def slam_down():
    global lock_in_timer
    for i in range(23):
        move_down()
    lock_in_timer = 25


def fall():
    global board
    if check_down() == False:
        return
    else:
        for cell in active_position:
            board[cell[0]][cell[1]] = 0
        for i in range(4):
            active_position[i][0] = active_position[i][0] + 1
        for cell in active_position:
            board[cell[0]][cell[1]] = tetromino_colour

def rotate(direction):
    global current_piece_orientation
    global current_piece_type
    global active_position

    if current_piece_type != "O":

        old_position = get_tetromino(current_piece_type,current_piece_orientation)

        # -- rotate clockwise --
        if direction == 0:
            current_piece_orientation += 1
        # -- rotate anti-clockwise --
        else:
            current_piece_orientation += -1

        current_piece_orientation = current_piece_orientation % 4
        checks = get_rotation_checks(current_piece_type, current_piece_orientation)
        new_position = get_tetromino(current_piece_type,current_piece_orientation)

        # RUN THE FIVE-O CHECK-Os
        # new_position = active_position
        # for i in range(5):
        #     for j in range (4):
        #         new_x = active_position[j][1] + checks[i][1]

        # -- perform the TRANSFORMATION
        for cell in active_position:
            board[cell[0]][cell[1]] = 0
        for i in range(4):
            # -- Subtract the old offsets and add the new offsetst to rotate whilst maintaining postions on the board
            active_position[i][1] = active_position[i][1] - old_position[i][0] + new_position[i][0]
            active_position[i][0] = active_position[i][0] - old_position[i][1] + new_position[i][1]
        for cell in active_position:
            board[cell[0]][cell[1]] = tetromino_colour


# --- load tetrominoes --- 
with open('tetrominoes.json') as jsonfile:
    tetrominoes = json.load(jsonfile)
    def get_tetromino(type, rotation):
        return tetrominoes.get(type)[rotation]
        
# --- load rotation checks --- 
with open('rotations.json') as jsonfile:
    rotation_checks = json.load(jsonfile)  
    def get_rotation_checks(tetromino_type, rotation):
        if tetromino_type in "JLSTZ":
            return rotation_checks.get("JLSTZ")[rotation]
        elif tetromino_type == "I":
            return rotation_checks.get("I")[rotation]
        return

# Spawn the initial tetronimo
spawn_tetromino()

# -- draw non-board pieces --
def draw_piece_image(pos_x, pos_y, piece):
    if piece != "":
        colour = convert_letter_to_colour(piece)
        coords = get_tetromino(piece, 0)
        offset_saved_x = 5
        offset_saved_y = 0
        if piece == "O":
            offset_saved_x = -15
        if piece == "I":
            offset_saved_x = -10
            offset_saved_y = -20
        for coord in coords:
            pygame.draw.rect(screen, colour, (pos_x + 50 + (coord[0] * 45) + offset_saved_x, pos_y + 50 + (coord[1] * 45) + offset_saved_y, width, width), 0)

def draw_saved():
    pygame.draw.rect(screen, "white", (saved_piece_pane_offset_x, saved_piece_pane_offset_y, 250, 150), 1)
    SECONDARY_FONT.render_to(screen, (saved_piece_pane_offset_x + 80, saved_piece_pane_offset_y + 10 ), "SAVED", (255, 255, 255))
    draw_piece_image(saved_piece_pane_offset_x, saved_piece_pane_offset_y, saved_piece_type)


def draw_upcoming():
    global bag

    pygame.draw.rect(screen, "white", (1300, saved_piece_pane_offset_y, 250, 660), 1)
    SECONDARY_FONT.render_to(screen, (1300 + 40, saved_piece_pane_offset_y + 10 ), "UPCOMING", (255, 255, 255))
    upcoming_y_off = saved_piece_pane_offset_y
    for i in range(5):
        if(len(bag) < 5):
            bag = bag + generate_bag()
        draw_piece_image(1300, upcoming_y_off, convert_to_tetromino_letter(bag[i]))
        upcoming_y_off += 120


bg = pygame.image.load("space.jpg")
# play_area = pygame.Surface((1920,1080))
# play_area.fill((255,255,255,1))
# play_area = pygame.draw.rect(screen, (255,255,255), (50, 50, 50, 50), 1)
# play_area = pygame.transform.gaussian_blur(play_area, 20)

# -------- Main Game Loop  -----------
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
            if event.key == pygame.K_SPACE:
                slam_down()
            if event.key == pygame.K_LSHIFT:
                save_symbol()
            if event.key == pygame.K_UP:
                rotate(0)
            if event.key == pygame.K_RCTRL or event.key == pygame.K_LCTRL:
                rotate(1)
 
    # --- Game logic should go here


    # gravity for active block
    frame_counter += 1
    if frame_counter % speed == 0:
        fall()
    
    if touch_bottom is True:
        lock_in_timer += 1
    else:
        lock_in_timer = 0
    
    if lock_in_timer == 30:
        print("LOCKING IN!")
        lock_in_timer = 0
        touch_bottom = False
        move_count = 0
        clear_lines(get_full_lines())
        check_death()
        spawn_tetromino()

 
    # --- Screen-clearing ---
    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.blit(bg, (0,0))

    # Draw Title
    GAME_FONT.render_to(screen, (100, 50), "TETRIS", (255, 255, 255))

    # --- Draw background animation ---
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

    check_down()

    # -- draw UI pieces ---
    draw_saved()
    draw_upcoming()

    # --- Draw game grid ---
    offset_x = offset_mid_x
    offset_y = offset_mid_y
    for row in range(board_height):
        offset_y += margin
        for column in range(board_width):
            draw = True
            if(board[row][column] != 0):
                colour = convert_letter_to_colour(board[row][column])
                filled = 0
            else:
                if row < 3:
                    draw = False
                else:
                    colour = "white"
                    filled = 1

            offset_x += margin
            if draw:
                pygame.draw.rect(screen, colour, (offset_x, offset_y, width, width), filled)
            offset_x += width
        offset_x = offset_mid_x
        offset_y += height


    # --- Update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)

 
# Close the window and quit.
pygame.quit()
