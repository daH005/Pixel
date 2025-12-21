from os import listdir
from pathlib import Path
from traceback import print_exc

from engine.common.files import del_extension
from engine.common.singleton import SingletonMeta
from engine.levels.level import Level

__all__ = (
    'LevelsManager',
)


class LevelsManager(metaclass=SingletonMeta):

    _levels: list[Level] = []
    _current_level: Level

    def __init__(self, levels_folder_path: Path) -> None:
        self._levels_folder_path = levels_folder_path
        self._levels_count: int = 0

    @property
    def levels(self) -> list[Level]:
        return list(self._levels)

    @property
    def current_level(self) -> Level:
        return self._current_level

    @property
    def last_index(self) -> int:
        return len(self._levels) - 1

    def init(self) -> None:
        filenames: list[str] = sorted(
            listdir(self._levels_folder_path),
            key=lambda x: int(del_extension(x)),
        )
        for filename in filenames:
            try:
                self.add_level(self._levels_folder_path.joinpath(filename))
            except ValueError:
                print_exc()
                continue

    def add_level(self, file_path: Path) -> None:
        level = Level(index=self._levels_count, file_path=file_path)
        self._levels_count += 1
        self._levels.append(level)

    def next_after(self, level_index: int) -> Level:
        if level_index != self.last_index:
            return self._levels[level_index + 1]
        return self._levels[level_index]

    def current_level_by_list(self) -> Level:
        for level in self._levels:
            if level.index == self.last_index:
                return level
            if level.is_available and not self.next_after(level.index).is_available:
                return level

    def switch_to(self, level_index: int) -> Level:
        self._current_level = self._levels[level_index]
        return self._current_level

    def go_next(self) -> Level:
        self._current_level = self.next_after(self._current_level.index)
        return self._current_level

    def set_current_as_completed(self) -> None:
        self._current_level.complete()
        self.next_after(self.current_level.index).open()
