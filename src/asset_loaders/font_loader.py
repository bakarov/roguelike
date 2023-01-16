import os
import pygame

from configs.assets import ASSETS_DIR, FONTS_DIR

def font_loader(font, font_size):
    return pygame.font.Font(os.path.join(ASSETS_DIR, FONTS_DIR, font), font_size)