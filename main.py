import pygame
import pygame.freetype
import json
import time
import asyncio
from board import Board
from render.starfield import Starfield
from managers.board_manager import BoardManager
from managers.settings_manager import SettingsManager
from multi.network_client import NetworkClient
import pygame_menu

# --- Gameplay vars ---
screen_width = 1920
screen_height = 1080
local_multi = False
online_multi = False
board_manager = None
name = "Player"

ASSETS = 'assets/'

# --- start up pygame ---
pygame.init()

pygame.freetype.init()
GAME_FONT = pygame.freetype.Font(ASSETS + "font/RobotoMono-Bold.ttf", 80)
TITLE_FONT = pygame.freetype.Font(ASSETS + "font/RobotoMono-Bold.ttf", 80)

pygame.display.set_caption("Tetris")

music = ASSETS + 'audio/theme.wav'
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load(music)

# Set the width and height of the screen [width, height]
size = (screen_width, screen_height)
screen = pygame.display.set_mode(size)

# Loop until the done
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

bg = pygame.image.load(ASSETS + "img/space.jpg")
starfield = Starfield(pygame, screen)

# blurrity blur
# play_area = pygame.Surface((1920,1080))
# play_area.fill((255,255,255,1))
# play_area = pygame.draw.rect(screen, (255,255,255), (50, 50, 50, 50), 1)
# play_area = pygame.transform.gaussian_blur(play_area, 20)

settings_manager = SettingsManager("assets/data/settings.json")

TITLE_FONT.render_to(screen, (1000, 500), "TETRIS", (255, 255, 255))

def start_solo():
    global board_manager
    global online_multi

    online_multi = False
    local_multi = False
    board_manager = BoardManager(screen, pygame, settings_manager, local_multi, online_multi, name)
    main()
    pass

def start_local_multi():
    global board_manager
    global online_multi

    online_multi = False
    local_multi = True
    board_manager = BoardManager(screen, pygame, settings_manager, local_multi, online_multi, name)
    main()
    pass

def start_online_multi():
    global board_manager
    global online_multi

    online_multi = True
    local_multi = False
    board_manager = BoardManager(screen, pygame, settings_manager, local_multi, online_multi, name)
    main()
    pass

def set_name(player_name):
    global name

    settings_manager.set_name(player_name)


async def main_menu():
    settings_menu = pygame_menu.Menu('SETTINGS', 400, 300,
                        theme=pygame_menu.themes.THEME_DARK)
    settings_menu.add.text_input('Online Name', default="Player", onchange=set_name)
    settings_menu.add.button('Resolution', start_local_multi)
    settings_menu.add.button('Volume', start_online_multi)
    settings_menu.add.button('Back to main menu', pygame_menu.events.BACK)

    menu = pygame_menu.Menu('TETRIS', 400, 300, theme=pygame_menu.themes.THEME_DARK)

    menu.add.button('Solo', start_solo)
    menu.add.button('2P Local', start_local_multi)
    menu.add.button('Online', start_online_multi)
    menu.add.button('Settings', settings_menu)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(screen)


def main():
    global frame_counter
    global touch_bottom
    global done
    global local_multi
    global online_multi
    global board_manager

    dead_timer = 0

    if online_multi:
        n = NetworkClient()
        b1 = n.getBoard()

    pygame.mixer.music.play(loops=-1)

# -------- Main Game Loop  -----------
    while not done:
        if online_multi:
            # --- receive player 2's position from the server ---
            board_manager.set_p2_board(n.send(board_manager.get_board()))
        if not board_manager.is_dead():
            # --- Screen clear ---
            screen.blit(bg, (0,0))
            # --- animate bg ---
            starfield.animate()
            # --- process board movements ---
            board_manager.check_movement()

            # Draw Title
            GAME_FONT.render_to(screen, (100, 50), "TETRIS", (255, 255, 255))

            # --- Update the screen with what we've drawn.
            pygame.display.flip()

            # --- Limit to 60 frames per second
            clock.tick(60)
        else:
            if(dead_timer >= 400):
                done = True

            GAME_FONT.render_to(screen, (775, 352), "GAME OVER", (255, 255, 255))
            # done = True
            # --- Update the screen with what we've drawn.
            pygame.display.flip()

            dead_timer += 1

            # --- Limit to 60 frames per second
            clock.tick(60)


    # return to main menu
    done = False
    main_menu()


asyncio.run( main_menu() )