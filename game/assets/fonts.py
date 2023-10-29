"""Здесь подключаются шрифты из папки 'assets/fonts'."""

from __future__ import annotations
from pygame.font import Font, init as init_pygame_font
from pathlib import Path
from typing import TypeAlias
from enum import IntEnum

from game.config import GameConfig

__all__ = (
    'FontsDict',
    'FONTS_PATH',
    'FontSize',
    'PIXEL_FONTS',
)

init_pygame_font()

FontsDict: TypeAlias = dict[int, Font]
FONTS_PATH: Path = GameConfig.ASSETS_PATH.joinpath('fonts')


class FontSize(IntEnum):
    SMALL = 20
    DEFAULT = 30
    LARGE = 40


def _prepare_fonts(filename: str, sizes: list[int]) -> FontsDict:
    full_path: Path = FONTS_PATH.joinpath(filename)
    fonts: FontsDict = {}
    for size in sizes:
        fonts[size] = Font(full_path, size)
    return fonts


PIXEL_FONTS: FontsDict = _prepare_fonts('pixel.ttf', list(FontSize))


if __name__ == '__main__':
    print(PIXEL_FONTS)
