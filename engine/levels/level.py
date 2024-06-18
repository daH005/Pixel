from pathlib import Path
from typing import Generic

from engine.common.files import save_json, load_json
from engine.levels.object_data_tuple import LevelObjectDataTuple
from engine.levels.level_data import LevelData
from engine.levels.typing_ import ExtraDataType

__all__ = (
    'Level',
)


class Level(Generic[ExtraDataType]):

    def __init__(self, index: int, file_path: Path) -> None:
        self._index = index
        self._file_path = file_path
        self._data: LevelData[ExtraDataType] = load_json(self._file_path)
        self._init_objects()

    def _init_objects(self) -> None:
        self._objects: list[LevelObjectDataTuple] = []
        for i, object_data in enumerate(self._data['objects']):
            self._objects.append(LevelObjectDataTuple(**object_data))

    @property
    def index(self) -> int:
        return self._index

    @property
    def objects(self) -> list[LevelObjectDataTuple]:
        return list(self._objects)

    @property
    def w(self) -> int:
        return self._data['w']

    @property
    def h(self) -> int:
        return self._data['h']

    @property
    def is_available(self) -> bool:
        return self._data['is_available']

    @property
    def is_completed(self) -> bool:
        return self._data['is_completed']

    @property
    def extra(self) -> ExtraDataType:
        return dict(self._data['extra_data'])

    def complete(self) -> None:
        self._data['is_completed'] = True
        self._save()

    def _save(self) -> None:
        save_json(self._file_path, self._data)

    def open(self) -> None:
        self._data['is_available'] = True
        self._save()

    def update_extra_data(self, **kwargs) -> None:
        self._data['extra_data'].update(**kwargs)
        self._save()
