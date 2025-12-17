import pygame as pg
from abc import ABC

from engine.common.direction import Direction
from game.assets.images import (
    DirtImages,
    PlayerDefaultImages,
    FINISH_IMAGE,
)

__all__ = (
    'AbstractEditorObject',
    'Dirt',
    'Player',
    'Finish',
)


class AbstractEditorObject(ABC):
    _image: pg.Surface

    def __init__(self, x: int, y: int) -> None:
        x -= self._image.get_width() // 2
        y -= self._image.get_height()
        self._rect = self._image.get_rect(x=x, y=y)
        self._screen = pg.display.get_surface()

    @property
    def x(self) -> int:
        return self._rect.x

    @property
    def y(self) -> int:
        return self._rect.y

    def get_rect(self) -> pg.Rect:
        return self._rect.copy()

    def data_to_compare(self):
        return type(self), self._rect.x, self._rect.y

    def update(self, x_offset: int, y_offset: int) -> None:
        self._screen.blit(self._image, (self._rect.x - x_offset, self._rect.y - y_offset))

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
            'x': self._rect.x,
            'y': self._rect.y,
        }


class Dirt(AbstractEditorObject):

    def __init__(self, x: int, y: int,
                 grass_enabled: bool = False,
                 direction: Direction | None = None,
                 ) -> None:
        self._direction = direction
        if self._direction == Direction.RIGHT:
            self._image = DirtImages.RIGHT
        elif self._direction == Direction.LEFT:
            self._image = DirtImages.LEFT
        else:
            self._image = DirtImages.DEFAULT

        self._grass_enabled = grass_enabled
        if self._grass_enabled:
            self._image = self._image.copy()
            self._image.blit(DirtImages.GRASS_LIST[1], (0, 0))

        super().__init__(x=x, y=y)

    def _make_json_args(self) -> dict:
        return {
            **super()._make_json_args(),
            'grass_enabled': self._grass_enabled,
            'direction': self._direction,
        }


class Player(AbstractEditorObject):
    _image = PlayerDefaultImages.STAND_RIGHT[0]


class Finish(AbstractEditorObject):
    _image = FINISH_IMAGE
