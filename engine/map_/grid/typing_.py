from typing import TypeAlias

__all__ = (
    'RangesType',
    'GridAttrsType',
)

RangesType: TypeAlias = tuple[tuple[int, int], tuple[int, int]]
GridAttrsType: TypeAlias = list[int]
