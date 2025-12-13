from abc import ABC

from engine.common.typing_ import AnyRectType
from engine.map_.grid.abstract_grid_object import AbstractGridObject

__all__ = (
    'AbstractMapObject',
)


class AbstractMapObject(AbstractGridObject, ABC):
    _Z_INDEX: int = 0

    def __init__(self, map_: 'Map',
                 rect: AnyRectType,
                 ) -> None:
        super().__init__(rect=rect)
        self._map = map_

    @property
    def z_index(self) -> int:
        return self._Z_INDEX

    def _draw(self) -> None:
        self._screen.blit(self._image, self._map.camera.apply(self._rect))

    @classmethod
    def reset_class(cls) -> None:
        pass


from engine.map_.map_ import Map
