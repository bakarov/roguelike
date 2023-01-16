import pygame


class Darkness:
    def __init__(self, screen):
        # Common
        self.screen = screen
        self.darkness = pygame.Surface(
            (self.screen.get_width(), self.screen.get_height()), flags=pygame.SRCALPHA
        )

        # Variables
        self.darkness_value = 0
        self.darkness_value_increase = 1

    # Each level the difficulty increases: the darkness appears faster through the multiplier
    def increase_multiplier(self, multiplier):
        self.darkness_value_increase *= multiplier

    def make_darker(self):
        self.darkness_value += self.darkness_value_increase
        self.darkness.fill(
            (self.darkness_value, self.darkness_value, self.darkness_value, 0)
        )

    def draw(self):
        self.screen.blit(self.darkness, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
