from typing import TypedDict, Generic

from engine.levels.object_data import LevelObjectData
from engine.levels.typing_ import ExtraDataType

__all__ = (
    'LevelData',
)


class LevelData(TypedDict, Generic[ExtraDataType]):

    objects: list[LevelObjectData]
    is_available: bool
    is_completed: bool
    w: int
    h: int
    extra_data: ExtraDataType
