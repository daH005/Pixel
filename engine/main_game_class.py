from pygame import quit
from pygame.time import Clock
from pygame.display import flip

from engine.exceptions import ExitFromGame
from engine.common.singleton import SingletonMeta
from engine.fps import init_max_fps
from engine.scenes.manager import ScenesManager

__all__ = (
    'Game',
)


class Game(metaclass=SingletonMeta):

    def __init__(self, max_fps: float,
                 scenes_manager: ScenesManager,
                 ) -> None:
        self._max_fps = max_fps
        init_max_fps(max_fps=self._max_fps)

        self._scenes_manager = scenes_manager
        self._scenes_manager.init()
        self._scenes_manager.levels_manager.init()

        self._clock: Clock = Clock()

    def run(self) -> None:
        while True:
            try:
                self._clock.tick(self._max_fps)
                self._scenes_manager.current_scene.update()
                flip()
            except ExitFromGame:
                break
        quit()
