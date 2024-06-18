import pygame
from pathlib import Path

__all__ = (
    'GameConfig',
)


class GameConfig:
    MAX_FPS: float = 60

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

    # Было принято решение использовать относительный импорт,
    # т.к. это облегчает работу и с '.py' и с '.exe'.
    ASSETS_PATH: Path = Path('../assets')
    LEVELS_PATH: Path = ASSETS_PATH.joinpath('levels')
    IMAGES_PATH: Path = ASSETS_PATH.joinpath('images')
    SOUNDS_PATH: Path = ASSETS_PATH.joinpath('sounds')
    FONTS_PATH: Path = ASSETS_PATH.joinpath('fonts')
