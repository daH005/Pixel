import pygame as pg

from engine.levels.manager import LevelsManager
from engine.screen import set_global_screen
from engine.main_game_class import Game
from game.assets.images import ICON_IMAGE
from game.config import GameConfig
from editor.scenes_manager import ScenesManager, EDITOR_SCENE_KEY


def main() -> None:
    flags = GameConfig.WINDOW_FLAGS & (~pg.FULLSCREEN)
    set_global_screen(GameConfig.WINDOW_HEIGHT, 'Editor', flags, ICON_IMAGE)

    game = Game(GameConfig.MAX_FPS, ScenesManager(EDITOR_SCENE_KEY, LevelsManager(GameConfig.LEVELS_PATH)))
    game.run()


if __name__ == '__main__':
    main()
