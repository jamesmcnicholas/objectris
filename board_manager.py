from board import Board
from board_renderer import BoardRenderer
import pygame

class BoardManager():
    def __init__(self, screen, pygame, settings_manager, multi):
        self.pygame = pygame
        self.settings_manager = settings_manager
        # TODO dynamic offsets for multiple boards
        self.board_p1 = Board(23, 10, -400)
        self.board_p2 = Board(23, 10, 400)
        self.frame_counter = 0
        self.speed = 60
        self.board_renderer = BoardRenderer(screen, pygame)
        self.multi = multi


    def check_movement(self):
        for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    done = True
                elif event.type == self.pygame.KEYDOWN:
                    if pygame.key.name(event.key) == self.settings_manager.get_keybind("p1_left"):
                        self.board_p1.move_left()
                    if pygame.key.name(event.key) == self.settings_manager.get_keybind("p1_right"):
                        self.board_p1.move_right()
                    if pygame.key.name(event.key) == self.settings_manager.get_keybind("p1_down"):
                        self.board_p1.move_down()
                    if pygame.key.name(event.key) == self.settings_manager.get_keybind("p1_slam"):
                        self.board_p1.slam_down()
                    if pygame.key.name(event.key) == self.settings_manager.get_keybind("p1_save_piece"):
                        self.board_p1.save_symbol()
                    if pygame.key.name(event.key) == self.settings_manager.get_keybind("p1_rotate_clockwise"):
                        self.board_p1.rotate(0)
                    if pygame.key.name(event.key) == self.settings_manager.get_keybind("p1_rotate_anticlockwise"):
                        self.board_p1.rotate(1)
                    
                    if not self.multi:
                        # --- p2 controls ---
                        if pygame.key.name(event.key) == self.settings_manager.get_keybind("p2_left"):
                            self.board_p2.move_left()
                        if pygame.key.name(event.key) == self.settings_manager.get_keybind("p2_right"):
                            self.board_p2.move_right()
                        if pygame.key.name(event.key) == self.settings_manager.get_keybind("p2_down"):
                            self.board_p2.move_down()
                        if pygame.key.name(event.key) == self.settings_manager.get_keybind("p2_slam"):
                            self.board_p2.slam_down()
                        if pygame.key.name(event.key) == self.settings_manager.get_keybind("p2_save_piece"):
                            self.board_p2.save_symbol()
                        if pygame.key.name(event.key) == self.settings_manager.get_keybind("p2_rotate_clockwise"):
                            self.board_p2.rotate(0)
                        if pygame.key.name(event.key) == self.settings_manager.get_keybind("p2_rotate_anticlockwise"):
                            self.board_p2.rotate(1)

        self.do_movement()

    def do_movement(self):
        # gravity for active block
        self.frame_counter += 1
        if self.frame_counter % self.speed == 0:
            self.board_p1.fall()
            if not self.multi:
                self.board_p2.fall()

        # -- player 1 checks --
        if self.board_p1.touch_bottom is True:
            self.board_p1.lock_in_timer += 1
        else:
            self.board_p1.lock_in_timer = 0

        if self.board_p1.lock_in_timer == 30:
            self.board_p1.lock_in_timer = 0
            self.board_p1.touch_bottom = False
            self.board_p1.move_count = 0

            self.board_p1.clear_lines(self.board_p1.get_full_lines())
            self.board_p1.check_death()
            self.board_p1.spawn_tetromino()

        if not self.multi:
            # -- player 2 checks --
            if self.board_p2.touch_bottom is True:
                self.board_p2.lock_in_timer += 1
            else:
                self.board_p2.lock_in_timer = 0

            if self.board_p2.lock_in_timer == 30:
                self.board_p2.lock_in_timer = 0
                self.board_p2.touch_bottom = False
                self.board_p2.move_count = 0

                self.board_p2.clear_lines(self.board_p2.get_full_lines())
                self.board_p2.check_death()
                self.board_p2.spawn_tetromino()

            self.board_p2.check_down()

        self.board_p1.check_down()
        

        self.board_renderer.draw(self.board_p1)
        self.board_renderer.draw(self.board_p2)

    def get_board(self):
        return self.board_p1

    def set_p2_board(self, board):
        self.board_p2 = board