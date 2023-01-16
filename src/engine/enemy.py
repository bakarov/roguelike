import pygame

from asset_loaders.animation_loader import animation_loader
from configs.window import TILESIZE
from configs.assets import ENEMY_ANIMATIONS, ENEMY_ANIMATIONS_DIR


class Enemy(pygame.sprite.Sprite):
    def __init__(self, camera, enemies, x, y, screen, direction):
        # Common
        pygame.sprite.Sprite.__init__(self, enemies)
        self.camera = camera
        self.screen = screen
        self.image = pygame.Surface((TILESIZE, TILESIZE)).convert_alpha()
        self.rect = self.image.get_rect()

        # Animations
        self.animatiom_images = {}
        self.animation_frames = {}
        for animation in ENEMY_ANIMATIONS:
            (
                self.animatiom_images[animation],
                self.animation_frames[animation],
            ) = animation_loader(ENEMY_ANIMATIONS_DIR, animation)
        self.current_animation = ENEMY_ANIMATIONS[0]
        self.current_frame = 0
        self.animation_flip = False

        # Moving
        self.x = x
        self.y = y
        self.direction = direction
        self.enemy_move_timer = pygame.time.get_ticks()
        self.enemy_direction_change_timer = pygame.time.get_ticks()

    def change_animation(self, new_animation):
        if self.current_animation != new_animation:
            self.current_animation = new_animation
            self.current_frame = 0

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

        self.current_frame += 1
        if self.current_frame >= len(self.animation_frames[self.current_animation]):
            self.current_frame = 0

        self.flip = False
        if self.direction["direction"] == "left":
            self.flip = True

    def draw(self):
        image_in_current_frame = self.animation_frames[self.current_animation][
            self.current_frame
        ]
        image = self.animatiom_images[self.current_animation][image_in_current_frame]
        self.screen.blit(
            pygame.transform.flip(image, self.animation_flip, False),
            self.camera.apply(self)
        )
