import pygame

from configs.window import WIDTH
from configs.colors import BLACK


class Button(object):
    def __init__(self, screen, x, y, text, font, color, center=True):
        super(Button, self).__init__()
        self.screen = screen
        self.x = x
        self.y = y
        self.text = font.render(text, True, color)
        self.button_color = BLACK

        if center:
            self.x = WIDTH / 2 - self.text.get_width() / 2

    def render(self):
        self.rect = pygame.draw.rect(
            self.screen,
            self.button_color,
            (self.x, self.y, self.text.get_width(), self.text.get_height()),
            0,
        )
        self.button = self.screen.blit(self.text, (self.x, self.y))
        return self

    def is_mouse_in(self, pos):
        if self.button.collidepoint(pos):
            return True
        else:
            return False
