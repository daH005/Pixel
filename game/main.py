"""Основной модуль, импортирующий сцены и запускающий окно игры."""

from pygame import quit
from pygame.display import flip

from game.scenes import ScenesManager, SceneKey, SceneKeyType
from game.contrib.exceptions import Exit
from game.contrib.singleton_ import SingletonMeta

__all__ = (
    'Game',
)


class Game(metaclass=SingletonMeta):
    """Класс-одиночка, метод `run()` которого запускает игру.
    В `__init__(...)` можно передать ключ начальной сцены.
    """

    def __init__(self, initial_scene_key: SceneKeyType = SceneKey.HOME) -> None:
        ScenesManager.switch(initial_scene_key)

    @staticmethod
    def run() -> None:
        while True:
            try:
                ScenesManager.current_scene.update()
                flip()
            except Exit:
                break
        quit()


if __name__ == '__main__':
    game: Game = Game()
    game.run()
