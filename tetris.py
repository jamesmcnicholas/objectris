import pygame
import json
import random
from random import randint
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

frame_counter = 0
speed = 60
tetromino_colour = ""

height = 20
width = 20
margin = 5
colour = "white"
bag = []
active_position = [[], [], [], []]

# --- build the board model --- #
board = []
for row in range (20):
    board.append([])
    for column in range(10):
        board[row].append(0)

pygame.init()

 
# Set the width and height of the screen [width, height]
size = (700, 500)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Tetris")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 

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

def move_left():
    global board
    board = [[0 for x in range(10)] for y in range(20)]
    for i in range(4):
        active_position[i][1] = active_position[i][1] - 1
    for cell in active_position:
        board[cell[0]][cell[1]] = tetromino_colour
    
def move_right():
    global board
    board = [[0 for x in range(10)] for y in range(20)]
    for i in range(4):
        active_position[i][1] = active_position[i][1] + 1
    for cell in active_position:
        board[cell[0]][cell[1]] = tetromino_colour

def move_down():
    global board
    board = [[0 for x in range(10)] for y in range(20)]
    for i in range(4):
        active_position[i][0] = active_position[i][0] + 1
    for cell in active_position:
        board[cell[0]][cell[1]] = tetromino_colour


def fall():
    global board
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
 
    # --- Screen-clearing code goes here
 
    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
 
    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(BLACK)
 
    # --- Drawing code should go here

    frame_counter += 1
    
    if frame_counter % speed == 0:
        print(frame_counter)
        fall()

    offset_x = 0
    offset_y = 0
    for row in range(20):
        offset_y += margin
        for column in range(10):

            if(board[row][column] != 0):
                colour = convert_letter_to_colour(tetromino_colour)
            else:
                colour = "white"

            offset_x += margin
            pygame.draw.rect(screen, colour, (offset_x, offset_y, width, width))
            offset_x += width
        offset_x = 0
        offset_y += height


    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)

 
# Close the window and quit.
pygame.quit()



