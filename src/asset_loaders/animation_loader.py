import os
import pygame

from configs.assets import ASSETS_DIR, GRAPHICS_DIR, ANIMATION_DURATION, ANIMATION_SIZE
from configs.colors import WHITE

def animation_loader(animation_dir, animation):
    animation_frames = []
    animation_images = {}
    animation_path = os.path.join(ASSETS_DIR, GRAPHICS_DIR, animation_dir, animation)
    
    for animation_image in os.listdir(animation_path):
        loaded_animation_image = pygame.transform.scale(pygame.image.load(os.path.join(animation_path, animation_image)).convert(), ANIMATION_SIZE)
        
        # make transparent
        loaded_animation_image.set_colorkey(WHITE)
        
        animation_images[animation_image] = loaded_animation_image.copy()
        animation_frames.extend([animation_image]*ANIMATION_DURATION)
    
    return animation_images, animation_frames