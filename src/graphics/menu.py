import pygame

from asset_loaders.font_loader import font_loader
from configs.assets import MAIN_FONT, MENU_TEXT_FONT_SIZE, MENU_BUTTON_FONT_SIZE
from configs.window import HEIGHT
from graphics.button import Button
from graphics.text import Text


class Menu(object):
    def __init__(self, screen, num_menu_items):
        super(Menu, self).__init__()
        self.items = []

        self.screen = screen
        self.items_positions_on_screen = [
            [
                ((HEIGHT - num_menu_items * 20 - 40) / num_menu_items * x)
                for x in range(num_menu_items)
            ][x]
            + 40
            for x in range(num_menu_items)
        ]

        self.font = font_loader(MAIN_FONT, MENU_TEXT_FONT_SIZE)
        self.button_font = font_loader(MAIN_FONT, MENU_BUTTON_FONT_SIZE)

    def update(self, event):
        # Listen to mouse clicks for every button
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                for button in self.items:
                    if button["type"] == "button" and button["object"].is_mouse_in(
                        pygame.mouse.get_pos()
                    ):
                        return button["state"]

    def add_button(self, text, triggered_state, color):
        current_item_index = len(self.items)
        self.items.append(
            {
                "type": "button",
                "object": Button(
                    self.screen,
                    0,
                    self.items_positions_on_screen[current_item_index],
                    text,
                    self.button_font,
                    color,
                ),
                "state": triggered_state,
            }
        )
        return self

    def add_text(self, text, color):
        current_item_index = len(self.items)
        self.items.append(
            {
                "type": "text",
                "object": Text(
                    self.screen,
                    0,
                    self.items_positions_on_screen[current_item_index],
                    text,
                    self.font,
                    color,
                ),
                "state": None,
            }
        )
        return self

    def render(self):
        for item in self.items:
            item["object"].render()
        return self
