import pygame as pg
from traceback import print_exc

from engine.levels.manager import LevelsManager
from engine.screen import set_global_screen
from engine.main_game_class import Game
from game.assets.images import ICON_IMAGE
from game.config import GameConfig
from editor.scenes_manager import ScenesManager, EDITOR_SCENE_KEY


def main() -> None:
    flags = GameConfig.WINDOW_FLAGS & (~pg.FULLSCREEN)
    set_global_screen(GameConfig.WINDOW_HEIGHT, 'Editor', flags, ICON_IMAGE)

    scenes_manager = ScenesManager(EDITOR_SCENE_KEY, LevelsManager(GameConfig.LEVELS_PATH))
    game = Game(GameConfig.MAX_FPS, scenes_manager)

    try:
        game.run()
    except:
        print_exc()
        scenes_manager.get(EDITOR_SCENE_KEY).save_map()


if __name__ == '__main__':
    main()
