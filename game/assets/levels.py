"""Модуль предоставляет класс `LevelsManager` для работы с уровнями
в разных частях проекта. Класс уровня - словарь `LevelData`.
Он реализован таким образом, чтобы при изменении значений свойств объекта (т.е. элементов словаря)
изменения фиксировались в соответствующем файле '.json'.
"""

from __future__ import annotations
from os import listdir
from pathlib import Path
from enum import StrEnum
from typing import TypeAlias, Any

from game.config import GameConfig
from game.contrib.dict_ import alias
from game.contrib.files import del_extension, load_json, save_json

__all__ = (
    'LEVELS_PATH',
    'LevelData',
    'LevelsListType',
    'ObjectData',
    'LevelsManager',
)

LEVELS_PATH: Path = GameConfig.ASSETS_PATH.joinpath('levels')


class LevelData(dict):

    class Key(StrEnum):
        OBJECTS = 'objects'
        IS_COMPLETED = 'is_completed'
        IS_AVAILABLE = 'is_available'
        W = 'w'
        H = 'h'
        UNCREATING_IDS = 'uncreating_ids'

    def __init__(self, index: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        for i, object_data in enumerate(self[self.Key.OBJECTS]):
            self[self.Key.OBJECTS][i] = ObjectData(**object_data)
        self.index = index

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.save()

    def __eq__(self, other: LevelData | Any) -> bool:
        if type(other) == type(self):
            return other.index == self.index
        return super().__eq__(other)

    def save(self) -> None:
        save_json(self.file_path, self)

    @property
    def file_path(self) -> Path:
        return LEVELS_PATH.joinpath(self.filename)

    @property
    def filename(self) -> str:
        return str(self.index) + '.json'

    objects: list[ObjectData] = alias(Key.OBJECTS)
    is_completed: bool = alias(Key.IS_COMPLETED)
    is_available: bool = alias(Key.IS_AVAILABLE)
    w: int = alias(Key.W)
    h: int = alias(Key.H)
    # В этот список входят ID монеток и сундуков.
    uncreating_ids: list[int] = alias(Key.UNCREATING_IDS)


class ObjectData(dict):

    class Key(StrEnum):
        TYPE = 'type'
        ARGS = 'args'
        FACTORY_METHOD = 'factory_method'

    type: str = alias(Key.TYPE)
    args: dict[str, int | str] = alias(Key.ARGS, default={})
    factory_method: str = alias(Key.FACTORY_METHOD, default='__call__')


LevelsListType: TypeAlias = list[LevelData]


def _load_all() -> LevelsListType:
    levels: LevelsListType = []
    for filename in listdir(LEVELS_PATH):
        try:
            full_level_path: Path = LEVELS_PATH.joinpath(filename)
            level_index: int = int(del_extension(filename))
            levels.append(LevelData(index=level_index, **load_json(full_level_path)))
        except ValueError:
            continue
    return levels


class LevelsManager:
    LEVELS: LevelsListType = _load_all()
    current_level: LevelData

    @classmethod
    def last_index(cls) -> int:
        return len(cls.LEVELS) - 1

    @classmethod
    def next_after(cls, level_index: int) -> LevelData:
        if level_index != cls.last_index():
            return cls.LEVELS[level_index + 1]
        return cls.LEVELS[level_index]

    @classmethod
    def current_level_on_list(cls) -> LevelData:
        for level in cls.LEVELS:
            if level.index == cls.last_index():
                return level
            if level.is_available and not cls.next_after(level.index).is_available:
                return level

    @classmethod
    def change(cls, level_index: int) -> LevelData:
        cls.current_level = cls.LEVELS[level_index]
        return cls.current_level

    @classmethod
    def go_next(cls) -> LevelData:
        cls.current_level = cls.next_after(cls.current_level.index)
        return cls.current_level

    @classmethod
    def set_current_as_completed(cls) -> None:
        cls.current_level.is_completed = True
        cls.next_after(cls.current_level.index).is_available = True


if __name__ == '__main__':
    LevelsManager.change(0)
    print(LevelsManager.current_level.index)
    print(LevelsManager.next_after(0).index)
    print(LevelsManager.next_after(0).index)
    print(LevelsManager.next_after(3).index)
    LevelsManager.go_next()
    print(LevelsManager.current_level.index)
    LevelsManager.go_next()
    LevelsManager.go_next()
    LevelsManager.go_next()
    LevelsManager.go_next()
    print(LevelsManager.current_level.index)
    LevelsManager.change(2)
    print(LevelsManager.current_level.index)
    print(LevelsManager.current_level_on_list().index)
