from pygame import Surface
from abc import ABC, abstractmethod

from engine.common.typing_ import AnyRectType
from engine.screen_access_mixin import ScreenAccessMixin

__all__ = (
    'AbstractUI',
    'AbstractNoSizeUI',
    'AbstractRectangularUI',
)


class AbstractUI(ScreenAccessMixin, ABC):
    _image: Surface

    def update(self) -> None:
        self._draw()

    @abstractmethod
    def _draw(self) -> None:
        pass


class AbstractNoSizeUI(AbstractUI):

    def __init__(self, x: int = 0, y: int = 0) -> None:
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    def _draw(self) -> None:
        self._screen.blit(self._image, (self._x, self._y))


class AbstractRectangularUI(AbstractUI):

    def __init__(self, rect: AnyRectType) -> None:
        self._rect = rect

    @property
    def x(self) -> int:
        return self._rect.x

    @property
    def y(self) -> int:
        return self._rect.y

    def get_rect(self) -> AnyRectType:
        return self._rect.copy()

    def update(self) -> None:
        self._update_image()
        self._draw()

    def _update_image(self) -> None:
        pass

    def _draw(self) -> None:
        self._screen.blit(self._image, self._rect)
