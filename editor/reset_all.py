from game.assets.levels import LevelsManager
from game.assets.save import save

if __name__ == '__main__':
    save.coins_count = 0
    for level in LevelsManager.LEVELS:
        level.is_available = False
        if level.index == 0:
            level.is_available = True
        level.is_completed = False
        level.uncreating_ids = []
