"""Модуль формирует готовый к работе класс `ScenesManager`."""

from game.scenes.base import ScenesManager, SceneKey, SceneKeyType
from game.scenes.home import HomeScene
from game.scenes.levels_menu import LevelsMenuScene
from game.scenes.level import LevelScene
from game.scenes.level_pause import LevelPauseScene
from game.scenes.level_losing import LevelLosingScene
from game.scenes.level_completion import LevelCompletionScene

__all__ = (
    'ScenesManager',
    'SceneKey',
    'SceneKeyType',
)
