from pygame import Surface, Rect
from abc import ABC

from engine.screen_access_mixin import ScreenAccessMixin
from engine.common.float_rect import FloatRect

__all__ = (
    'AbstractUI',
)


class AbstractUI(ScreenAccessMixin, ABC):
    _image: Surface

    def __init__(self, rect: Rect | FloatRect | None = None) -> None:
        self._rect = rect

    def get_rect(self) -> Rect | FloatRect:
        # AttributeError: 'FloatRect' object has no attribute 'float_x'
        return self._rect.copy()

    def update(self) -> None:
        self._update_image()
        self._draw()

    def _update_image(self) -> None:
        pass

    def _draw(self) -> None:
        self._screen.blit(self._image, self._rect)
