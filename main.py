import pygame
import pygame.freetype
import json
import random
from random import randint
import time
import asyncio
from board import Board, generate_bag, convert_letter_to_colour, convert_to_tetromino_letter
from starfield import Starfield

# --- Gameplay vars ---
frame_counter = 0
speed = 60
screen_width = 1920
screen_height = 1080

# --- start up pygame ---

pygame.init()
pygame.freetype.init()
# GAME_FONT = pygame.freetype.Font("RobotoMono-Bold.ttf", 80)
# SECONDARY_FONT = pygame.freetype.Font("RobotoMono-Bold.ttf", 30)



# Set the width and height of the screen [width, height]
size = (screen_width, screen_height)
screen = pygame.display.set_mode(size)

# Generate the board
board = Board(screen, 0, pygame)

pygame.display.set_caption("Tetris")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

bg = pygame.image.load("space.jpg")
starfield = Starfield(pygame, screen)

# play_area = pygame.Surface((1920,1080))
# play_area.fill((255,255,255,1))
# play_area = pygame.draw.rect(screen, (255,255,255), (50, 50, 50, 50), 1)
# play_area = pygame.transform.gaussian_blur(play_area, 20)


async def main():
    global frame_counter
    global touch_bottom
    global done

# -------- Main Game Loop  -----------
    while not done:
        # --- Main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    board.move_left()
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    board.move_right()
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    board.move_down()
                if event.key == pygame.K_SPACE:
                    board.slam_down()
                if event.key == pygame.K_LSHIFT:
                    board.save_symbol()
                if event.key == pygame.K_UP:
                    board.rotate(0)
                if event.key == pygame.K_RCTRL or event.key == pygame.K_LCTRL:
                    board.rotate(1)

        # gravity for active block
        frame_counter += 1
        if frame_counter % speed == 0:
            board.fall()
        
        if board.touch_bottom is True:
            board.lock_in_timer += 1
        else:
            board.lock_in_timer = 0
        
        if board.lock_in_timer == 30:
            board.lock_in_timer = 0
            board.touch_bottom = False
            move_count = 0
            board.clear_lines(board.get_full_lines())
            board.check_death()
            board.spawn_tetromino()


        # --- Screen-clearing ---
        # Here, we clear the screen to white. Don't put other drawing commands above this
        screen.blit(bg, (0,0))
        starfield.animate()

        # Draw Title
        # GAME_FONT.render_to(screen, (100, 50), "TETRIS", (255, 255, 255))

        board.check_down()

        # -- draw board
        board.draw()


        # --- Update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)
        await asyncio.sleep(0)


    # Close the window and quit.
    pygame.quit()


asyncio.run( main() )