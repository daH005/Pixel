from engine.levels.manager import LevelsManager
from game.assets.save import set_coins_count
from game.config import GameConfig

if __name__ == '__main__':
    set_coins_count(0)

    levels_manager: LevelsManager = LevelsManager(levels_folder_path=GameConfig.LEVELS_PATH)
    levels_manager.init()

    for level in levels_manager.levels:
        level.close()

    levels_manager.levels[0].open()
