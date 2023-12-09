import pygame
import pygame.freetype
import json
import random
from random import randint
import time
import asyncio
from board import Board, generate_bag, convert_letter_to_colour, convert_to_tetromino_letter
from starfield import Starfield
from board_manager import BoardManager
from settings_manager import SettingsManager

# --- Gameplay vars ---
screen_width = 1920
screen_height = 1080

# --- start up pygame ---
pygame.init()

pygame.freetype.init()
GAME_FONT = pygame.freetype.Font("RobotoMono-Bold.ttf", 80)

pygame.display.set_caption("Tetris")

# Set the width and height of the screen [width, height]
size = (screen_width, screen_height)
screen = pygame.display.set_mode(size)

# Loop until the done
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

bg = pygame.image.load("space.jpg")
starfield = Starfield(pygame, screen)

# blurrity blur
# play_area = pygame.Surface((1920,1080))
# play_area.fill((255,255,255,1))
# play_area = pygame.draw.rect(screen, (255,255,255), (50, 50, 50, 50), 1)
# play_area = pygame.transform.gaussian_blur(play_area, 20)

settings_manager = SettingsManager("settings.json")
board_manager = BoardManager(screen, pygame, settings_manager)


async def main():
    global frame_counter
    global touch_bottom
    global done

# -------- Main Game Loop  -----------
    while not done:
        # --- Main event loop


        # --- Screen-clearing ---
        # Here, we clear the screen to white. Don't put other drawing commands above this
        screen.blit(bg, (0,0))
        starfield.animate()

        board_manager.check_movement()

        # Draw Title
        GAME_FONT.render_to(screen, (100, 50), "TETRIS", (255, 255, 255))


        # --- Update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)
        await asyncio.sleep(0)


    # Close the window and quit.
    pygame.quit()


asyncio.run( main() )