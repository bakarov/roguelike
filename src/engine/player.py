import pygame

from configs.assets import SOUND_FOOTSTEP_1, SOUND_FOOTSTEP_2, PLAYER_ANIMATIONS, PLAYER_ANIMATIONS_DIR
from configs.window import TILESIZE
from asset_loaders.animation_loader import animation_loader
from asset_loaders.sound_loader import sound_loader


class Player(pygame.sprite.Sprite):
    def __init__(self, sprites, camera, x, y, screen, direction):
        # Common
        pygame.sprite.Sprite.__init__(self, sprites)
        self.camera = camera
        self.screen = screen
        self.image = pygame.Surface((TILESIZE, TILESIZE)).convert_alpha()
        self.rect = self.image.get_rect()

        # Animations
        self.animatiom_images = {}
        self.animation_frames = {}
        for animation in PLAYER_ANIMATIONS:
            self.animatiom_images[animation], self.animation_frames[animation] = animation_loader(
                PLAYER_ANIMATIONS_DIR, animation)
        self.current_animation = PLAYER_ANIMATIONS[0]
        self.current_frame = 0
        self.animation_flip = False

        # Sounds
        self.sound_frame = 1
        self.sound_timer = pygame.time.get_ticks()
        self.sound_1 = sound_loader(SOUND_FOOTSTEP_1)
        self.sound_2 = sound_loader(SOUND_FOOTSTEP_2)

        # Moving
        self.x = x
        self.y = y
        self.direction = direction

    def change_animation(self, new_animation):
        if self.current_animation != new_animation:
            self.current_animation = new_animation
            self.current_frame = 0

    def play_sound(self):
        if pygame.time.get_ticks() - self.sound_timer > 200:
            self.sound_timer = pygame.time.get_ticks()

            if self.sound_frame == 1:
                self.sound_1.play()
                self.sound_frame = 0

            elif self.sound_frame == 0:
                self.sound_2.play()
                self.sound_frame = 1

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

        self.current_frame += 1
        if self.current_frame >= len(self.animation_frames[self.current_animation]):
            self.current_frame = 0

        self.animation_flip = False
        if self.direction['direction'] == 'left':
            self.animation_flip = True

    def draw(self):
        image_in_current_frame = self.animation_frames[self.current_animation][self.current_frame]
        image = self.animatiom_images[self.current_animation][image_in_current_frame]
        self.screen.blit(pygame.transform.flip(
            image, self.animation_flip, False), self.camera.apply(self))
