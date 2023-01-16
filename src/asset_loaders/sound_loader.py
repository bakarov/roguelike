import os
import pygame

from configs.assets import ASSETS_DIR, SOUNDS_DIR

def sound_loader(sound_name):
    return pygame.mixer.Sound(os.path.join(ASSETS_DIR, SOUNDS_DIR, sound_name))