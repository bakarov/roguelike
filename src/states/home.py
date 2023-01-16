from asset_loaders.font_loader import font_loader
from asset_loaders.sound_loader import sound_loader

from graphics.menu import Menu

from configs.assets import SOUND_MENU_SELECT, MAIN_FONT, FONT_SIZE
from configs.colors import BLACK, GREY, WHITE
from configs.meta import TITLE, AUTHOR, VERSION, DATE
from configs.texts import HOME_MENU_PLAY_TEXT, HOME_MENU_QUIT_TEXT
from configs.variables import PLAY_STATE, QUIT_STATE, GAME_STATE
from configs.window import MAIN_INFO_PANEL_POSITION

import pygame


class Home(object):
    def __init__(self, screen):
        # Common
        self.screen = screen

        # Assets
        self.menu_select_sound = sound_loader(SOUND_MENU_SELECT)
        self.font = font_loader(MAIN_FONT, FONT_SIZE)

        # Menu
        self.home = Menu(self.screen, num_menu_items=3)
        self.home.add_text(TITLE, WHITE)
        self.home.add_button(HOME_MENU_PLAY_TEXT, PLAY_STATE, GREY)
        self.home.add_button(HOME_MENU_QUIT_TEXT, QUIT_STATE, GREY)

        # State
        self.returned_state = None

    def reset(self):
        self.returned_state = None

    def update(self):
        return self.returned_state, None

    def draw(self):
        # TODO: move to decorator
        self.screen.fill(BLACK)
        self.home.render()

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
            res = self.home.update(event)
            if res == PLAY_STATE:
                self.menu_select_sound.play()
                self.returned_state = GAME_STATE
            elif res == QUIT_STATE:
                self.menu_select_sound.play()
                pygame.quit()
