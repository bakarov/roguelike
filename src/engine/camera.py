import pygame

from configs.window import WIDTH, HEIGHT


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        # Limit scrolling to the dungeon size
        self.camera = pygame.Rect(
            max(-(self.width - WIDTH), min(0, -target.rect.centerx + int(WIDTH / 2))),
            max(
                -(self.height - HEIGHT), min(0, -target.rect.centery + int(HEIGHT / 2))
            ),
            self.width,
            self.height,
        )
