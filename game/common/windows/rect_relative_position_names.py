from enum import StrEnum

__all__ = (
    'RectRelativePositionName',
)


class RectRelativePositionName(StrEnum):
    TOPLEFT = 'topleft'
    TOPRIGHT = 'topright'
    BOTTOMLEFT = 'bottomleft'
    BOTTOMRIGHT = 'bottomright'
    MIDLEFT = 'midleft'
    MIDRIGHT = 'midright'
    MIDTOP = 'midtop'
    MIDBOTTOM = 'midbottom'
    CENTER = 'center'
