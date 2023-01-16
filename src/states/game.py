from asset_loaders.font_loader import font_loader
from asset_loaders.sound_loader import sound_loader

from engine.engine import Engine
from engine.camera import Camera
from engine.generator import Generator

from configs.assets import SOUND_GAME_OVER, SOUND_NEXT_LEVEL, MAIN_FONT
from configs.colors import WHITE, BLACK
from configs.meta import AUTHOR, VERSION, DATE
from configs.settings import DUNGEON_SIZE, STARTING_SCORE
from configs.texts import INFO_CURRENT_LEVEL_TEXT
from configs.variables import GAME_OVER_STATE, NEXT_LEVEL_STATE
from configs.window import TILESIZE, LEVEL_INFO_PANEL_POSITION, MAIN_INFO_PANEL_POSITION

import pygame


class Game(object):
    def __init__(self, screen):
        # Common
        self.screen = screen
        self.camera = Camera(
            TILESIZE * TILESIZE * DUNGEON_SIZE, TILESIZE * TILESIZE * DUNGEON_SIZE
        )
        self.generator = Generator()

        # Assets
        self.font = font_loader(MAIN_FONT, 10)
        self.sound_game_over = sound_loader(SOUND_GAME_OVER)
        self.sound_next_level = sound_loader(SOUND_NEXT_LEVEL)

        # Game
        self.score = STARTING_SCORE
        self.new_level()

    def reset(self):
        self.score = STARTING_SCORE
        self.new_level()

    def new_level(self):
        self.engine = Engine(self.camera, self.screen)
        self.engine.create_dungeon_object(self.generator.generate_maps(DUNGEON_SIZE))
        self.engine.place_player()
        self.engine.set_difficulty(self.score)

    def update(self):
        state = self.engine.update()

        if state == GAME_OVER_STATE:
            self.sound_game_over.play()
            return GAME_OVER_STATE, self.score

        if state == NEXT_LEVEL_STATE:
            self.sound_next_level.play()
            self.score += 1
            self.new_level()

        self.camera.update(self.engine.get_player())
        self.text = self.font.render(
            INFO_CURRENT_LEVEL_TEXT + str(self.score), True, WHITE
        )

        return None, None

    def draw(self):
        self.screen.fill(BLACK)  # TODO: move to a decorator

        # Draw objects
        self.engine.draw()

        # Show level info
        self.screen.blit(self.text, LEVEL_INFO_PANEL_POSITION)

        # TODO: Move to decorator
        info_text = "{}, {}. v{}".format(AUTHOR, DATE, VERSION)
        self.screen.blit(
            self.font.render(info_text, True, WHITE), MAIN_INFO_PANEL_POSITION
        )

        pygame.display.flip()

    def events(self):

        # TODO: move to decorator
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                # Player movement
                if event.key == pygame.K_LEFT:
                    self.engine.move_player("left")
                elif event.key == pygame.K_RIGHT:
                    self.engine.move_player("right")
                elif event.key == pygame.K_UP:
                    self.engine.move_player("up")
                elif event.key == pygame.K_DOWN:
                    self.engine.move_player("down")
                # Misc
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.engine.idle_player("right")
                elif event.key == pygame.K_LEFT:
                    self.engine.idle_player("left")
                elif event.key == pygame.K_UP:
                    self.engine.idle_player("up")
                elif event.key == pygame.K_DOWN:
                    self.engine.idle_player("down")
