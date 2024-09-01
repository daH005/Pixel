from pygame import Rect
from abc import ABC

from engine.common.float_rect import FloatRect
from engine.map_.grid.typing_ import AttrsType
from engine.map_.grid.abstract_grid_object import AbstractGridObject

__all__ = (
    'AbstractMapObject',
)


class AbstractMapObject(AbstractGridObject, ABC):
    _DEFAULT_Z_INDEX: int = 0

    def __init__(self, map_: 'Map',
                 rect: Rect | FloatRect | None = None,
                 attrs: AttrsType | None = None,
                 z_index: int | None = None,
                 ) -> None:
        if z_index is None:
            z_index = self._DEFAULT_Z_INDEX

        super().__init__(rect=rect, attrs=attrs)
        self._map = map_
        self._z_index = z_index

    @property
    def z_index(self) -> int:
        return self._z_index

    def _draw(self) -> None:
        self._screen.blit(self._image, self._map.camera.apply(self._rect))

    @classmethod
    def reset_class(cls) -> None:
        pass


from engine.map_.map_ import Map
