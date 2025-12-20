from pygame import Surface

from engine.map_.map_ import Map
from game.map_.abstract_ui import AbstractMapObject
from game.map_.z_indexes import ZIndex

__all__ = (
    'Overlay',
)


@Map.add_object_type
class Overlay(AbstractMapObject):

    _Z_INDEX = ZIndex.OVERLAY
    _ALPHA: int = 100

    def __init__(self, map_: Map,
                 x: int, y: int,
                 w: int, h: int,
                 ) -> None:
        self._w: int = w
        self._h: int = h
        self._init_image()
        super().__init__(
            map_=map_,
            rect=self._image.get_rect(x=x, y=y),
        )

    def _init_image(self) -> None:
        self._image = Surface((self._w, self._h))
        self._image.set_alpha(self._ALPHA)
