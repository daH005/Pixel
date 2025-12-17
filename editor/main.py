import pygame as pg

from engine.levels.manager import LevelsManager
from engine.screen import set_global_screen
from engine.main_game_class import Game
from game.assets.images import ICON_IMAGE
from game.config import GameConfig
from editor.scenes_manager import ScenesManager


def main() -> None:
    flags = GameConfig.WINDOW_FLAGS & (~pg.FULLSCREEN)
    set_global_screen(720, 'Editor', flags, ICON_IMAGE)

    game = Game(200, ScenesManager(0, LevelsManager(GameConfig.LEVELS_PATH)))
    game.run()


if __name__ == '__main__':
    main()
