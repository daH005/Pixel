from typing import TypedDict, Generic

from engine.common.typing_ import CameraBoundingLinesType
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
    camera_bounding_horizontal_lines: CameraBoundingLinesType
    extra_data: ExtraDataType
