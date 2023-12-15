import json
import random

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


class Board():
    def __init__(self, board_height, board_width, offset):
        self.board = []
        self.active_position = [[], [], [], []]
        self.speed = 60
        self.tetromino_colour = ""
        self.margin = 5
        self.colour = "white"
        self.bag = []
        self.touch_bottom = False
        self.lock_in_timer = 0
        self.move_count = 0
        self.saved_piece_type = ""
        self.current_piece_type = ""
        self.place_holder = ""
        self.has_swapped_piece = False
        self.current_piece_orientation = 0
        self.offset = offset
        self.board_height = board_height
        self.board_width = board_width
        
        # Build the board
        for row in range (self.board_height):
            self.board.append([])
            for column in range(self.board_width):
                self.board[row].append(0)

        # Get things going
        self.spawn_tetromino()


    def spawn_tetromino(self):
        # if third row is clear
        if self.board[2] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
            self.spawn(1,False)
        # else if second row is clear
        elif self.board[1] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
            self.spawn(0,False)


    def spawn_saved_piece(self):
            # if third row is clear
        if self.board[2] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
            self.spawn(1,True)
        # else if second row is clear
        elif self.board[1] == [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
            self.spawn(0,True)


    def spawn(self, row_offset,is_saved_piece):
        self.active_position = [[],[],[],[]]
        if is_saved_piece:
            letter = self.saved_piece_type
        else:
            self.has_swapped_piece = False
            if self.bag == []:
                self.generate_bag()
            letter = convert_to_tetromino_letter(self.bag.pop(0))
        tetromino = get_tetromino(letter,0)
        self.tetromino_colour = letter
        for cell in tetromino:
            self.board[cell[1]+row_offset][cell[0]+3] = self.tetromino_colour
        for i in range(4):
            self.active_position[i].append(tetromino[i][1]+row_offset)
            self.active_position[i].append(tetromino[i][0]+3)
        self.current_piece_type = letter
        self.current_piece_orientation = 0


    def save_symbol(self):
        if self.has_swapped_piece is False:
            if self.saved_piece_type == "":
                self.saved_piece_type = self.current_piece_type
                for i in range(4):
                    self.board[self.active_position[i][0]][self.active_position[i][1]] = 0
                self.spawn_tetromino()
            else:
                self.place_holder = self.current_piece_type
                for i in range(4):
                    self.board[self.active_position[i][0]][self.active_position[i][1]] = 0
                self.spawn_saved_piece()
                self.saved_piece_type = self.place_holder
                self.has_swapped_piece = True


    # --- scan for movement ---
    def check_left(self):
        for i in range(4):
            if self.active_position[i][1] - 1 < 0:
                return False
        for j in range(4):
            pos = self.active_position[j]
            # ensure we're not checking this piece's squares
            if [pos[0],pos[1]-1] not in self.active_position:
                if self.board[pos[0]][pos[1]-1] != 0:
                    touch_bottom = True
                    return False

    def check_right(self):
        for i in range(4):
            if self.active_position[i][1] + 1 > 9:
                return False
        for j in range(4):
            pos = self.active_position[j]
            # ensure we're not checking this piece's squares
            if [pos[0],pos[1]+1] not in self.active_position:
                if self.board[pos[0]][pos[1]+1] != 0:
                    touch_bottom = True
                    return False

    def check_down(self):
        # --- check for bottom of the board ---
        for i in range(4):
            pos = self.active_position[i]
            if pos[0] + 1 > self.board_height - 2:
                self.touch_bottom = True
            else:
                self.touch_bottom = False
            if pos[0] + 1 > self.board_height - 1:
                return False

        # --- check for pieces below this piece ---
        for j in range(4):
            pos = self.active_position[j]
            # ensure we're not checking this piece's squares
            if [pos[0]+1,pos[1]] not in self.active_position:
                if self.board[pos[0] + 1][pos[1]] != 0:
                    self.touch_bottom = True
                    return False


    def check_death(self):
        if self.board[1] != [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]:
            print("LOSER!!!!!")
    #         self.pygame.quit()


    def get_full_lines(self):
        list_full_lines = []
        for i in range(self.board_height):
            if not 0 in self.board[i]:
                list_full_lines.append(i)
        return list_full_lines


    # Shift down lines above the cleared line
    def clear_lines(self, full_lines):
        # For each full line, starting with the lowest
        for line in full_lines:
            # create an empty buffer
            buffer = [0] * self.board_width
            # loop through every line starting with the bottom full line, going up
            # e.g. line 17 is full, loop 17,16,15....1,0
            for i in range(line,0,-1):
                # set buffer to the above line
                buffer = self.board[i-1]
                # set this line to the buffer
                self.board[i] = buffer
            # Clear the top line
            self.board[0] = [0] * self.board_width


    # --- move active block ---
    def move_left(self):
        if self.check_left() == False:
            return
        else:
            if self.touch_bottom is True:
                self.move_count += 1
            if self.move_count < 14:
                self.lock_in_timer = 0
            for cell in self.active_position:
                self.board[cell[0]][cell[1]] = 0
            for i in range(4):
                self.active_position[i][1] = self.active_position[i][1] - 1
            for cell in self.active_position:
                self.board[cell[0]][cell[1]] = self.tetromino_colour


    def move_right(self):
        if self.check_right() == False:
            return
        else:
            if self.touch_bottom is True:
                self.move_count += 1
            if self.move_count < 14:
                self.lock_in_timer = 0
            for cell in self.active_position:
                self.board[cell[0]][cell[1]] = 0
            for i in range(4):
                self.active_position[i][1] = self.active_position[i][1] + 1
            for cell in self.active_position:
                self.board[cell[0]][cell[1]] = self.tetromino_colour


    def move_down(self):
        if self.check_down() == False:
            return
        else:
            for cell in self.active_position:
                self.board[cell[0]][cell[1]] = 0
            for i in range(4):
                self.active_position[i][0] = self.active_position[i][0] + 1
            for cell in self.active_position:
                self.board[cell[0]][cell[1]] = self.tetromino_colour


    def slam_down(self):
        for i in range(23):
            self.move_down()
        self.lock_in_timer = 25


    def fall(self):
        if self.check_down() == False:
            return
        else:
            for cell in self.active_position:
                self.board[cell[0]][cell[1]] = 0
            for i in range(4):
                self.active_position[i][0] = self.active_position[i][0] + 1
            for cell in self.active_position:
                self.board[cell[0]][cell[1]] = self.tetromino_colour


    def rotate(self, direction):
        if self.current_piece_type != "O":
            old_position = get_tetromino(self.current_piece_type,self.current_piece_orientation)

            # -- rotate clockwise --
            if direction == 0:
                self.current_piece_orientation += 1
            # -- rotate anti-clockwise --
            else:
                self.current_piece_orientation += -1

            self.current_piece_orientation = self.current_piece_orientation % 4
            checks = get_rotation_checks(self.current_piece_type, self.current_piece_orientation)
            new_position = get_tetromino(self.current_piece_type, self.current_piece_orientation)

            # RUN THE FIVE-O CHECK-Os
            # new_position = active_position
            # for i in range(5):
            #     for j in range (4):
            #         new_x = active_position[j][1] + checks[i][1]

            # -- perform the TRANSFORMATION
            for cell in self.active_position:
                self.board[cell[0]][cell[1]] = 0
            for i in range(4):
                # -- Subtract the old offsets and add the new offsetst to rotate whilst maintaining postions on the board
                self.active_position[i][1] = self.active_position[i][1] - old_position[i][0] + new_position[i][0]
                self.active_position[i][0] = self.active_position[i][0] - old_position[i][1] + new_position[i][1]
            for cell in self.active_position:
                self.board[cell[0]][cell[1]] = self.tetromino_colour
    
    def generate_bag(self):
        self.bag = self.bag + random.sample(range(0, 7), 7)

    def set_offset(self, offset):
        self.offset = offset