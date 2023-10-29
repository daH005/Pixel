"""Модуль выполняет `pygame.init()` и создаёт окно (а точнее поверхность `screen`) игры."""

from pygame import init as init_pygame, Surface, display, Rect

from game.contrib.annotations import SizeTupleType
from game.config import GameConfig
from game.assets.images import ICON_IMAGE

__all__ = (
    'screen',
    'SCREEN_RECT',
    'SCREEN_SIZE',
    'SCREEN_W',
    'SCREEN_H',
)

init_pygame()


def _new_screen() -> Surface:
    screen_: Surface = display.set_mode(_prepare_window_size(), flags=GameConfig.WINDOW_FLAGS)
    display.set_caption(GameConfig.WINDOW_TITLE)
    display.set_icon(ICON_IMAGE)
    return screen_


def _prepare_window_size() -> tuple[int, int]:
    return _calc_window_w(), GameConfig.WINDOW_HEIGHT


def _calc_window_w() -> int:
    screen_info = display.Info()
    return int(GameConfig.WINDOW_HEIGHT * (screen_info.current_w / screen_info.current_h))


screen: Surface = _new_screen()
# Зашьём основные параметры окна в константы, чтобы не вызывать методы `screen` каждый раз.
SCREEN_RECT: Rect = screen.get_rect()
SCREEN_SIZE: SizeTupleType = screen.get_size()
SCREEN_W: int = screen.get_width()
SCREEN_H: int = screen.get_height()
