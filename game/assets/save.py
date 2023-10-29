"""Модуль предоставляет класс-одиночку `Save` для работы с файлом 'assets/save.json'."""

from enum import StrEnum
from pathlib import Path

from game.contrib.singleton_ import SingletonMeta
from game.contrib.dict_ import alias
from game.contrib.files import save_json, load_json
from game.config import GameConfig

__all__ = (
    'Save',
    'save',
)


class Save(dict, metaclass=SingletonMeta):
    FILE_PATH: Path = GameConfig.ASSETS_PATH.joinpath('save.json')

    class Key(StrEnum):
        COINS_COUNT = 'coins_count'

    def __init__(self) -> None:
        super().__init__(load_json(self.FILE_PATH))

    def __setitem__(self, key, value) -> None:
        super().__setitem__(key, value)
        self.save()

    def save(self) -> None:
        save_json(self.FILE_PATH, self)

    coins_count: int = alias(Key.COINS_COUNT)


save: Save = Save()

if __name__ == '__main__':
    print(save)
    save.coins_count += 5
