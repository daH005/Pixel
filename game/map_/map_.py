from typing import Callable

from game.assets.levels import LevelData, ObjectData, LevelsManager
from game.assets.save import save
from game.contrib.singleton_ import SingletonMeta
from game.map_.exceptions import MapObjectCannotBeCreated
from game.map_.camera import Camera
from game.map_.grid import Grid, SomeMapObjectType

__all__ = (
    'Map',
)


class Map(metaclass=SingletonMeta):
    OBJECTS_TYPES: dict[str, type[SomeMapObjectType]] = {}
    level: LevelData
    player: SomeMapObjectType

    def __init__(self) -> None:
        self.camera: Camera = Camera()
        self.grid: Grid = Grid()
        # Не путать с `level.is_completed` и др. свойствами `LevelData`!
        self.is_completed: bool = False
        self.uncreating_ids: list[int] = []
        self.taken_coins_count: int = 0
        self.visual_taken_coins_count: int = 0

    def reset(self) -> None:
        self.level = LevelsManager.current_level
        self._reset_grid()
        self._reset_camera()
        self.is_completed = False
        self.uncreating_ids.clear()
        self.taken_coins_count = 0
        self.visual_taken_coins_count = 0

    def _reset_grid(self) -> None:
        self.grid.reset(
            LevelsManager.current_level.w,
            LevelsManager.current_level.h,
        )
        for object_data in self.level.objects:
            self.add_object_by_data(object_data)

    def add_object_by_data(self, object_data: ObjectData) -> None:
        try:
            object_ = self._new_object_by_data(object_data)
            self.grid.add(object_)
        except MapObjectCannotBeCreated:
            pass

    def _new_object_by_data(self, object_data: ObjectData) -> SomeMapObjectType:
        object_type: type[SomeMapObjectType] = self.OBJECTS_TYPES[object_data.type]
        factory_method: Callable = getattr(object_type, object_data.factory_method)
        return factory_method(**object_data.args)

    def _reset_camera(self) -> None:
        self.camera.reset(
            LevelsManager.current_level.w,
            LevelsManager.current_level.h,
        )
        self.camera.central_rect = self.player.rect
        self.camera.move_quick()

    def update(self) -> None:
        self.camera.update()
        self.grid.update()
        for object_ in self._sorted_visible_objects():
            object_.update()

    def _sorted_visible_objects(self) -> list[SomeMapObjectType]:
        return sorted(self.grid.visible_objects, key=lambda x: x.Z_INDEX)

    def finish(self) -> None:
        LevelsManager.set_current_as_completed()
        self.is_completed = True
        self.level.uncreating_ids = [
            *self.level.uncreating_ids,
            *self.uncreating_ids,
        ]
        save.coins_count += self.taken_coins_count

    @classmethod
    def add_object_type(cls, type_: type[SomeMapObjectType]) -> type[SomeMapObjectType]:
        cls.OBJECTS_TYPES[type_.__name__] = type_
        return type_
