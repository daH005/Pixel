from typing import TypeVar

from engine.map_.abstract_map_object import AbstractMapObject

__all__ = (
    'PlayerType',
)

PlayerType = TypeVar('PlayerType', bound=AbstractMapObject)
