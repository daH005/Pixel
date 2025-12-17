import pygame as pg
from abc import ABC

from game.assets.images import (
    DirtImages,
)

__all__ = (
    'AbstractEditorObject',
    'Dirt',
)


class AbstractEditorObject(ABC):
    _image: pg.Surface

    def __init__(self, x: int, y: int) -> None:
        self._x = x
        self._y = y
        self._screen = pg.display.get_surface()

    def data_to_compare(self):
        return type(self), self._x, self._y

    def update(self, x_offset: int, y_offset: int) -> None:
        self._screen.blit(self._image, (self._x - x_offset, self._y - y_offset))

    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return super().__eq__(other)
        return self.data_to_compare() == other.data_to_compare()

    def to_json(self) -> dict:
        return {
            'type': type(self).__name__,
            'factory_method': '__call__',
            'args': self._make_json_args(),
        }

    def _make_json_args(self) -> dict:
        return {
            'x': self._x,
            'y': self._y,
        }


class Dirt(AbstractEditorObject):
    _image = DirtImages.DEFAULT
