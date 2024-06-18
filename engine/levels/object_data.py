from typing import TypedDict

__all__ = (
    'LevelObjectData',
)


class LevelObjectData(TypedDict):

    type: str
    args: dict[str, int | str]
    factory_method: str
