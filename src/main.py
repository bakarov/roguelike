from configs.meta import TITLE
from configs.variables import GAME_STATE, HOME_STATE, GAME_OVER_STATE
from configs.window import WIDTH, HEIGHT

from states.home import Home
from states.game_over import GameOver
from states.game import Game

import pygame


if __name__ == "__main__":
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    pygame.key.set_repeat(500, 100)

    pygame.mixer.quit()
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)

    home = Home(screen)
    game = Game(screen)
    game_over = GameOver(screen)

    states = {HOME_STATE: home, GAME_STATE: game, GAME_OVER_STATE: game_over}

    current_state = HOME_STATE

    while True:
        # Track keyboard during state running
        states[current_state].events()

        # Track updates from the state
        state_update, state_artifact = states[current_state].update()

        # Render the state
        states[current_state].draw()

        if state_update is not None:
            states[current_state].reset()
            current_state = state_update

        if state_artifact is not None and current_state == GAME_OVER_STATE:
            game_over.update_score(state_artifact)
