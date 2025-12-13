from typing import TypeVar
from abc import ABC

from engine.common.typing_ import AnyRectType
from engine.abstract_ui import AbstractRectangularUI
from engine.map_.grid.typing_ import GridAttrsType

__all__ = (
    'AbstractGridObject',
    'AnyGridObjectType',
)


class AbstractGridObject(AbstractRectangularUI, ABC):
    _GRID_ATTRS: GridAttrsType = []

    def __init__(self, rect: AnyRectType) -> None:
        super().__init__(rect=rect)
        self._to_delete: bool = False

    @property
    def to_delete(self) -> bool:
        return self._to_delete

    @property
    def grid_attrs(self) -> GridAttrsType:
        return self._GRID_ATTRS


AnyGridObjectType = TypeVar('AnyGridObjectType', bound=AbstractGridObject)
