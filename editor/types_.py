import pygame as pg
from abc import ABC

from engine.common.direction import Direction
from game.assets.images import (
    DirtImages,
    PlayerDefaultImages,
    FINISH_IMAGE,
    TREES_IMAGES,
    COIN_IMAGES,
    CHEST_IMAGES,
    HINT_IMAGES,
)
from game.assets.fonts import PixelFonts

__all__ = (
    'AbstractEditorObject',
    'Dirt',
    'Player',
    'Finish',
    'Tree',
    'AbstractEditorObjectToDisposableCollect',
    'Coin',
    'Chest',
    'Hint',
)


class AbstractEditorObject(ABC):
    _image: pg.Surface

    def __init__(self, x: int, y: int) -> None:
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

    def attach_rect_position_to_bottom_center_of_block(self, block_size: int) -> None:
        self._rect.x += block_size // 2 - self._image.get_width() // 2
        self._rect.y += block_size - self._image.get_height()

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

    _DEFAULT_IMAGE = DirtImages.DEFAULT
    _RIGHT_IMAGE = DirtImages.RIGHT
    _LEFT_IMAGE = DirtImages.LEFT
    _GRASS_IMAGE = DirtImages.GRASS_LIST[1]

    def __init__(self, x: int, y: int,
                 grass_enabled: bool = False,
                 direction: Direction | None = None,
                 ) -> None:
        self._direction = direction
        if self._direction == Direction.RIGHT:
            self._image = self._RIGHT_IMAGE
        elif self._direction == Direction.LEFT:
            self._image = self._LEFT_IMAGE
        else:
            self._image = self._DEFAULT_IMAGE

        self._grass_enabled = grass_enabled
        if self._grass_enabled:
            self._image = self._image.copy()
            self._image.blit(self._GRASS_IMAGE, (0, 0))

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


class Tree(AbstractEditorObject):
    _IMAGE_VARIANTS = TREES_IMAGES

    def __init__(self, x: int, y: int, image_index: int = 0) -> None:
        self._image_index = image_index
        self._image = self._IMAGE_VARIANTS[self._image_index]
        super().__init__(x, y)

    def _make_json_args(self) -> dict:
        return {
            **super()._make_json_args(),
            'image_index': self._image_index,
        }


class AbstractEditorObjectToDisposableCollect(AbstractEditorObject):
    _class_id_count: int = 0

    def __init__(self, x: int, y: int, id_: int | None = None) -> None:
        super().__init__(x, y)
        self._id = id_
        if self._id is not None:
            t = AbstractEditorObjectToDisposableCollect
            t._class_id_count = max(t._class_id_count, self._id + 1)
            self._add_id_on_image()

    def set_id(self) -> None:
        t = AbstractEditorObjectToDisposableCollect
        self._id = t._class_id_count
        t._class_id_count += 1
        self._add_id_on_image()

    def _add_id_on_image(self) -> None:
        self._image = self._image.copy()
        id_image = PixelFonts.SMALL.render(str(self._id), 1, (0, 0, 0))
        self._image.blit(id_image, (0, 0))

    def _make_json_args(self) -> dict:
        return {
            **super()._make_json_args(),
            'id_': self._id,
        }


class Coin(AbstractEditorObjectToDisposableCollect):
    _image = COIN_IMAGES[0]


class Chest(AbstractEditorObjectToDisposableCollect):
    _image = CHEST_IMAGES[0]


class Hint(AbstractEditorObject):
    _image = HINT_IMAGES[0]

    def __init__(self, x: int, y: int, text: str | None = None) -> None:
        super().__init__(x, y)
        if text is None:
            text = input('Enter text of the hint: ')
        self._text = text

    def _make_json_args(self) -> dict:
        return {
            **super()._make_json_args(),
            'text': self._text,
        }
