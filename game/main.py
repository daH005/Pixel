from engine.screen import set_global_screen
from engine.levels.manager import LevelsManager
from engine.main_game_class import Game
from game.scenes import ScenesManager
from game.scenes.keys import SceneKey
from game.assets.images import ICON_IMAGE
from game.config import GameConfig

if __name__ == '__main__':
    set_global_screen(
        h=GameConfig.WINDOW_HEIGHT,
        title=GameConfig.WINDOW_TITLE,
        flags=GameConfig.WINDOW_FLAGS,
        icon=ICON_IMAGE,
    )
    game: Game = Game(
        max_fps=GameConfig.MAX_FPS,
        scenes_manager=ScenesManager(
            initial_scene_key=SceneKey.HOME,
            levels_manager=LevelsManager(
                levels_folder_path=GameConfig.LEVELS_PATH,
            ),
        ),
    )
    game.run()
