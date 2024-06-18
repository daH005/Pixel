from typing import TypeVar
from pygame import Rect
from abc import ABC

from engine.abstract_ui import AbstractUI
from engine.common.float_rect import FloatRect
from engine.map_.grid.typing_ import AttrsType

__all__ = (
    'AbstractGridObject',
    'AnyGridObjectType',
)


class AbstractGridObject(AbstractUI, ABC):

    def __init__(self, rect: Rect | FloatRect | None = None,
                 attrs: AttrsType | None = None,
                 ) -> None:
        super().__init__(rect=rect)
        if attrs is None:
            attrs = []

        self._to_delete = False
        self._attrs = attrs

    @property
    def to_delete(self) -> bool:
        return self._to_delete

    @property
    def attrs(self) -> AttrsType:
        return list(self._attrs)


AnyGridObjectType = TypeVar('AnyGridObjectType', bound=AbstractGridObject)
