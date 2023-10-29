from pygame import Surface, Rect
from abc import ABC

from game.contrib.screen import screen
from game.contrib.annotations import XYTupleType
from game.contrib.rects import FloatRect

__all__ = (
    'AbstractUI',
)


class AbstractUI(ABC):
    """Высший класс в иерархии UI.
    Реализует базовые вещи, такие как рисование и позиционирование.
    """

    image: Surface
    rect: Rect | FloatRect | XYTupleType

    def update(self) -> None:
        self._draw()

    def _draw(self) -> None:
        screen.blit(self.image, self.rect)
