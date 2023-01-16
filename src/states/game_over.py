import pygame

from asset_loaders.font_loader import font_loader
from asset_loaders.sound_loader import sound_loader

from graphics.menu import Menu

from configs.assets import SOUND_MENU_SELECT, MAIN_FONT, FONT_SIZE
from configs.colors import RED, BLACK, WHITE, GREY
from configs.meta import AUTHOR, VERSION, DATE
from configs.texts import (
    GAME_OVER_MENU_MAIN_TEXT,
    GAME_OVER_MENU_INFO_TEXT,
    GAME_OVER_MENU_PLAY_AGAIN_TEXT,
    GAME_OVER_MENU_QUIT_TEXT,
)
from configs.variables import PLAY_STATE, QUIT_STATE, GAME_STATE
from configs.window import MAIN_INFO_PANEL_POSITION


class GameOver(object):
    def __init__(self, screen):
        # Common
        self.screen = screen

        # Assets
        self.menu_select_sound = sound_loader(SOUND_MENU_SELECT)
        self.font = font_loader(MAIN_FONT, FONT_SIZE)

        # Objects
        self.main_menu = None
        self.returned_state = None

    def reset(self):
        self.returned_state = None

    def update_score(self, score):
        self.main_menu = Menu(self.screen, num_menu_items=4)
        self.main_menu.add_text(GAME_OVER_MENU_MAIN_TEXT, RED)
        self.main_menu.add_text(GAME_OVER_MENU_INFO_TEXT + str(score), WHITE)
        self.main_menu.add_button(GAME_OVER_MENU_PLAY_AGAIN_TEXT, PLAY_STATE, GREY)
        self.main_menu.add_button(GAME_OVER_MENU_QUIT_TEXT, QUIT_STATE, GREY)

    def update(self):
        return self.returned_state, None

    def draw(self):
        # TODO: move to decorator
        self.screen.fill(BLACK)
        self.main_menu.render()

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

            res = self.main_menu.update(event)
            if res == PLAY_STATE:
                self.menu_select_sound.play()
                self.returned_state = GAME_STATE
            elif res == QUIT_STATE:
                self.menu_select_sound.play()
                pygame.quit()
