from typing import NamedTuple

__all__ = (
    'LevelObjectDataTuple',
)


class LevelObjectDataTuple(NamedTuple):

    type: str
    args: dict[str, int | str]
    factory_method: str = '__call__'
