import random

# --- define star colours ---
LIGHTGREY = (192, 192, 192)
DARKGREY = (128, 128, 128)
YELLOW = (224, 224, 224)


class Starfield():
    def __init__(self, pygame, screen):

        self.star_field_slow = []
        self.star_field_medium = []
        self.star_field_fast = []
        self.screen_height = screen.get_height()
        self.screen_width = screen.get_width()
        self.pygame = pygame
        self.screen = screen

        for slow_stars in range(50): #birth those plasma balls, baby
            star_loc_x = random.randrange(0, self.screen_width)
            star_loc_y = random.randrange(0, self.screen_height)
            self.star_field_slow.append([star_loc_x, star_loc_y]) #i love your balls

        for medium_stars in range(35):
            star_loc_x = random.randrange(0, self.screen_width)
            star_loc_y = random.randrange(0, self.screen_height)
            self.star_field_medium.append([star_loc_x, star_loc_y])

        for fast_stars in range(15):
            star_loc_x = random.randrange(0, self.screen_width)
            star_loc_y = random.randrange(0, self.screen_height)
            self.star_field_fast.append([star_loc_x, star_loc_y])

    def animate(self):
        # --- Draw background animation ---
        for star in self.star_field_slow:
            star[1] += 1
            if star[1] > self.screen_height:
                star[0] = random.randrange(0, self.screen_width)
                star[1] = random.randrange(-20, -5)
            self.pygame.draw.circle(self.screen, DARKGREY, star, 3)

        for star in self.star_field_medium:
            star[1] += 4
            if star[1] > self.screen_height:
                star[0] = random.randrange(0, self.screen_width)
                star[1] = random.randrange(-20, -5)
            self.pygame.draw.circle(self.screen, LIGHTGREY, star, 2)

        for star in self.star_field_fast:
            star[1] += 8
            if star[1] > self.screen_height:
                star[0] = random.randrange(0, self.screen_width)
                star[1] = random.randrange(-20, -5)
            self.pygame.draw.circle(self.screen, YELLOW, star, 1)
