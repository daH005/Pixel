from typing import TypeAlias

__all__ = (
    'RangesType',
    'AttrsType',
)

RangesType: TypeAlias = tuple[tuple[int, int], tuple[int, int]]
AttrsType: TypeAlias = list[int]
