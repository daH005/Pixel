from pygame.font import Font

from game.config import GameConfig


__all__ = (
    'PixelFonts',
)


def load_font(size: int, font_name: str = 'pixel') -> Font:
    return Font(GameConfig.FONTS_PATH.joinpath(font_name + '.ttf'), size)


class PixelFonts:
    LARGE = load_font(40)
    MEDIUM = load_font(30)
    SMALL = load_font(20)
    VERY_SMALL = load_font(10)
