from board import convert_to_tetromino_letter, get_tetromino

CELL_HEIGHT = 40
CELL_WIDTH = 40


class BoardRenderer():
    def __init__(self, screen, pygame):
        self.screen = screen    
        self.offset_mid_x = self.screen.get_width()/2 - (CELL_WIDTH*5)
        self.offset_mid_y = self.screen.get_height()/2 - (CELL_HEIGHT*13)
        self.saved_piece_pane_offset_x = 500
        self.saved_piece_pane_offset_y = self.offset_mid_y * 8
        self.pygame = pygame
        self.SECONDARY_FONT = self.pygame.freetype.Font("assets/font/RobotoMono-Bold.ttf", 30)



    def draw_saved(self, board):
        self.pygame.draw.rect(self.screen, "white", (self.saved_piece_pane_offset_x + board.offset, self.saved_piece_pane_offset_y, 250, 150), 1)
        self.SECONDARY_FONT.render_to(self.screen, (self.saved_piece_pane_offset_x + 80 +  board.offset, self.saved_piece_pane_offset_y + 10 ), "SAVED", (255, 255, 255))
        self.draw_piece_image(self, self.saved_piece_pane_offset_x + board.offset, self.saved_piece_pane_offset_y, board.saved_piece_type)


    def draw_upcoming(self, board):
        self.pygame.draw.rect(self.screen, "white", (self.saved_piece_pane_offset_x +  board.offset, self.saved_piece_pane_offset_y + 235, 250, 660), 1)
        self.SECONDARY_FONT.render_to(self.screen, (self.saved_piece_pane_offset_x + 40 +  board.offset, self.saved_piece_pane_offset_y + 245 ), "UPCOMING", (255, 255, 255))
        upcoming_y_off = self.saved_piece_pane_offset_y + 235
        #TODO RUH ROH NOT A RENDERER THING, TAKE OUT THIS LOGIC
        for i in range(5):
            if(len(board.bag) < 5):
                board.generate_bag()
            self.draw_piece_image(self, self.saved_piece_pane_offset_x +  board.offset, upcoming_y_off, convert_to_tetromino_letter(board.bag[i]))
            upcoming_y_off += 120


    def draw_piece_image(self, board, pos_x, pos_y, piece):
        if piece != "":
            colour = self.convert_letter_to_colour(piece)
            coords = get_tetromino(piece, 0)
            offset_saved_x = 5
            offset_saved_y = 0
            if piece == "O":
                offset_saved_x = -15
            if piece == "I":
                offset_saved_x = -10
                offset_saved_y = -20
            for coord in coords:
                self.pygame.draw.rect(self.screen, colour, (pos_x + 50 + (coord[0] * 45) + offset_saved_x, pos_y + 50 + (coord[1] * 45) + offset_saved_y, CELL_WIDTH, CELL_WIDTH), 0)


    def draw_board(self, board):
        # --- Draw game grid ---
        offset_x = self.offset_mid_x + board.offset
        offset_y = self.offset_mid_y
        for row in range(board.board_height):
            offset_y += board.margin
            for column in range(board.board_width):
                draw = True
                if(board.board[row][column] != 0):
                    colour = self.convert_letter_to_colour(board.board[row][column])
                    filled = 0
                else:
                    if row < 3:
                        draw = False
                    else:
                        colour = "white"
                        filled = 1

                offset_x += board.margin
                if draw:
                    self.pygame.draw.rect(self.screen, colour, (offset_x, offset_y, CELL_WIDTH, CELL_WIDTH), filled)
                offset_x += CELL_WIDTH
            offset_x = self.offset_mid_x + board.offset
            offset_y += CELL_HEIGHT

    def draw_name(self, board):
        self.SECONDARY_FONT.render_to(self.screen, (self.saved_piece_pane_offset_x  + board.offset, self.saved_piece_pane_offset_y - 50 ), board.name, (255, 255, 255))

    def draw(self, board):
        self.draw_board(board)
        self.draw_upcoming(board)
        self.draw_saved(board)
        self.draw_name(board)

    def convert_letter_to_colour(self, letter):
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