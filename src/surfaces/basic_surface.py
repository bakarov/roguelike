import pygame
from configs.window import TILESIZE


class BasicSurface(pygame.sprite.Sprite):
    def __init__(self, sprites, surface_type, x, y):
        pygame.sprite.Sprite.__init__(self, sprites, surface_type)

        self.image = pygame.Surface((TILESIZE, TILESIZE))

        self.rect = self.image.get_rect()

        self.x = x
        self.y = y

        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
