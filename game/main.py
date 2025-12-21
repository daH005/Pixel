from pathlib import Path

from engine.screen import set_global_screen
from engine.levels.manager import LevelsManager
from engine.main_game_class import Game
from game.scenes import ScenesManager
from game.scenes.keys import SceneKey
from game.assets.images import ICON_IMAGE
from game.config import GameConfig

__all__ = (
    'start_game',
)


def start_game() -> None:
    set_global_screen(
        h=GameConfig.WINDOW_HEIGHT,
        title=GameConfig.WINDOW_TITLE,
        flags=GameConfig.WINDOW_FLAGS,
        icon=ICON_IMAGE,
    )

    levels_manager: LevelsManager = LevelsManager(
        levels_folder_path=GameConfig.LEVELS_PATH,
    )
    initial_scene_key = SceneKey.HOME

    game: Game = Game(
        max_fps=GameConfig.MAX_FPS,
        scenes_manager=ScenesManager(
            initial_scene_key=initial_scene_key,
            levels_manager=levels_manager,
        ),
    )
    game.run()


if __name__ == '__main__':
    start_game()
