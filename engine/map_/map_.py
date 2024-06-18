from typing import Callable

from engine.common.singleton import SingletonMeta
from engine.exceptions import MapObjectCannotBeCreated
from engine.screen_access_mixin import ScreenAccessMixin
from engine.levels.manager import LevelsManager
from engine.levels.object_data_tuple import LevelObjectDataTuple
from engine.levels.level import Level
from engine.map_.camera import Camera
from engine.map_.grid.grid import Grid

__all__ = (
    'Map',
)


class Map(ScreenAccessMixin, metaclass=SingletonMeta):

    _objects_types: dict[str, type['AbstractMapObject']] = {}
    _current_level: Level
    _player: 'PlayerType'

    def __init__(self, camera: Camera,
                 grid: Grid,
                 levels_manager: LevelsManager,
                 ) -> None:
        self._camera = camera
        self._grid = grid
        self._levels_manager = levels_manager
        self._is_completed: bool = False

    @property
    def camera(self) -> Camera:
        return self._camera

    @property
    def grid(self) -> Grid:
        return self._grid

    @property
    def levels_manager(self) -> LevelsManager:
        return self._levels_manager

    @property
    def is_completed(self) -> bool:
        return self._is_completed

    @property
    def player(self) -> 'PlayerType':
        return self._player

    @classmethod
    def add_object_type(cls, type_: type['AbstractMapObject']) -> type['AbstractMapObject']:
        cls._objects_types[type_.__name__] = type_
        return type_

    def reset(self) -> None:
        self._current_level = self._levels_manager.current_level
        self._reset_objects_types()
        self._reset_grid()
        self._reset_camera()
        self._is_completed = False

    def _reset_objects_types(self) -> None:
        for type_ in self._objects_types.values():
            type_.reset_class()

    def _reset_camera(self) -> None:
        self._camera.reset(
            self._levels_manager.current_level.w,
            self._levels_manager.current_level.h,
        )
        self._camera.move_quick(central_rect=self._player.get_rect())

    def _reset_grid(self) -> None:
        self._grid.reset(
            self._levels_manager.current_level.w,
            self._levels_manager.current_level.h,
        )
        for object_data in self._current_level.objects:
            self._add_object(object_data)

    def _add_object(self, object_data: LevelObjectDataTuple) -> None:
        try:
            object_ = self._new_object(object_data)
        except MapObjectCannotBeCreated:
            return

        self._grid.add(object_)
        if object_data.type == 'Player':
            self._player = object_

    def _new_object(self, object_data: LevelObjectDataTuple) -> 'AbstractMapObject':
        object_type: type[AbstractMapObject] = self._objects_types[object_data.type]
        factory_method: Callable = getattr(object_type, object_data.factory_method)
        return factory_method(map_=self, **object_data.args)

    def update(self) -> None:
        self._camera.update(central_rect=self._player.get_rect())
        self._grid.update()
        for object_ in self._sorted_visible_objects():
            object_.update()

    def _sorted_visible_objects(self) -> list['AbstractMapObject']:
        return sorted(self._grid.visible_objects, key=lambda x: x.z_index)

    def finish(self) -> None:
        self._levels_manager.set_current_as_completed()
        self._is_completed = True


from engine.map_.abstract_map_object import AbstractMapObject
from engine.map_.typing_ import PlayerType
