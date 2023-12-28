import pygame


class SoundManager():
        def __init__(self):
            SOUND_DIR = 'assets/audio/'

            self.click_sound = pygame.mixer.Sound(SOUND_DIR + "click.wav")
            self.bubble_sound = pygame.mixer.Sound(SOUND_DIR + "bubble.wav")
            self.bonk_sound = pygame.mixer.Sound(SOUND_DIR +"bonk2.wav")

        def click(self):
            pygame.mixer.Channel(1).play(self.click_sound)
        
        def bubble(self):
            pygame.mixer.Channel(1).play(self.bubble_sound)

        def bonk(self):
            pygame.mixer.Channel(1).play(self.bonk_sound)
