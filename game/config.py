"""В данном модуле собрана основная конфигурация игры."""

import pygame
from pathlib import Path as Path_

__all__ = (
    'GameConfig',
)


class GameConfig:
    WINDOW_TITLE: str = 'Pixel'
    # От высоты зависит масштаб игры, моделей.
    WINDOW_HEIGHT: int = 720
    WINDOW_FLAGS: int = (
        # Первые два флага способствуют оптимизации FPS.
        pygame.HWSURFACE |
        pygame.DOUBLEBUF |
        # Масштабируемость экрана по всему доступному размеру.
        pygame.SCALED |
        pygame.FULLSCREEN
    )
    MAX_FPS: float = 60
    # Было принято решение использовать относительный импорт,
    # т.к. это облегчает работу и с '.py' и с '.exe'.
    ASSETS_PATH: Path_ = Path_('../assets')
