from __future__ import annotations
from pygame import Rect
from pygame.mouse import get_pos
from typing import TypeVar, TypeAlias

from game.map_.abstract_ui import AbstractMapObject
from game.contrib.screen import SCREEN_W, SCREEN_H
from game.map_.map_ import Map as BaseMap
from game.map_.camera import Camera as BaseCamera
from game.map_.grid import Grid as BaseGrid
from game.contrib.annotations import XYTupleType
from game.assets.levels import LevelsManager, LevelData

__all__ = (
    'Map',
    'Camera',
    'Grid',
    'AbstractEditorMapObject',
    'SomeEditorMapObjectType',
    'MapObjectArgsJsonType',
    'MapObjectJsonType',
    'MapObjectsJsonType',
    'MapJsonType',
    'DEFAULT_FACTORY_METHOD_NAME',
)

MapObjectArgsJsonType: TypeAlias = dict[str, int | str]
MapObjectJsonType: TypeAlias = dict[str, str | MapObjectArgsJsonType]
MapObjectsJsonType: TypeAlias = list[MapObjectJsonType]
MapJsonType: TypeAlias = dict[str, int | bool | MapObjectsJsonType]
DEFAULT_FACTORY_METHOD_NAME: str = '__call__'


class AbstractEditorMapObject(AbstractMapObject):
    grid_x_list: list

    def __init__(self, x: int, y: int,
                 factory_method_name: str = DEFAULT_FACTORY_METHOD_NAME,
                 ) -> None:
        super().__init__(x, y)
        self.factory_method_name = factory_method_name

    @classmethod
    def new_with_coords_fix(cls, *args, **kwargs) -> AbstractEditorMapObject:
        return cls(*args, **kwargs)

    def serialize(self) -> MapObjectJsonType:
        return dict(
            type=type(self).__name__,
            factory_method=self.factory_method_name,
            args=self._prepare_args(),
        )

    def _prepare_args(self) -> MapObjectArgsJsonType:
        return dict(
            x=self.rect.x,
            y=self.rect.y,
        )

    def remove(self) -> None:
        self.grid_x_list.remove(self)


SomeEditorMapObjectType: TypeVar = TypeVar('SomeEditorMapObjectType',
                                           bound=AbstractEditorMapObject,
                                           covariant=True)


class Map(BaseMap):
    BLOCK_SCALE: int = 40
    level: LevelData | None
    w: int
    h: int

    class MapScrolling:
        SPEED: int = 15
        MAP_MOVING_BORDER_LEN: int = 50
        rect: Rect = Rect(0, 0, SCREEN_W, SCREEN_H)
        map_w: int
        map_h: int

        def reset(self, map_w: int, map_h: int) -> None:
            self.map_w = map_w
            self.map_h = map_h

        def update(self) -> None:
            mos_x_y: XYTupleType = get_pos()
            if mos_x_y[0] <= self.MAP_MOVING_BORDER_LEN and self.rect.left >= 0:
                self.rect.x -= self.SPEED
            if mos_x_y[0] >= SCREEN_W - self.MAP_MOVING_BORDER_LEN and self.rect.right <= self.map_w:
                self.rect.x += self.SPEED
            if mos_x_y[1] <= self.MAP_MOVING_BORDER_LEN and self.rect.top >= 0:
                self.rect.y -= self.SPEED
            if mos_x_y[1] >= SCREEN_H - self.MAP_MOVING_BORDER_LEN and self.rect.bottom <= self.map_h:
                self.rect.y += self.SPEED

    def __init__(self) -> None:
        super().__init__()
        self.camera: Camera = Camera()
        self.grid: Grid = Grid()
        self.map_scrolling = self.MapScrolling()

    def reset(self) -> None:
        self._load_level()
        self.map_scrolling.reset(self.w, self.h)
        self._reset_grid()
        self._reset_camera()

    def _reset_grid(self) -> None:
        self.grid.reset(self.w, self.h)
        if self.level:
            for object_data in self.level.objects:
                self.add_object_by_data(object_data)

    def _reset_camera(self) -> None:
        self.camera.reset(self.w, self.h)
        self.camera.central_rect = self.map_scrolling.rect
        self.camera.move_quick()

    def _load_level(self) -> None:
        level_index: str = input('Ввод: индекс уровня либо ENTER - ')
        if level_index:
            self.level: LevelData = LevelsManager.LEVELS[int(level_index)]
            self.w: int = self.level.w
            self.h: int = self.level.h
        else:
            self.level: None = None
            self.w: int = SCREEN_W
            self.h: int = SCREEN_H

    def update(self) -> None:
        self.map_scrolling.update()
        super().update()

    def prepare_json(self) -> MapJsonType:
        return dict(
            objects=self._prepare_objects(),
            is_available=True,
            is_completed=False,
            w=self.w,
            h=self.h,
            uncreating_ids=[],
        )

    def _prepare_objects(self) -> MapObjectsJsonType:
        objects = []
        for y_row in self.grid:
            for x_cell in y_row:
                for obj in x_cell:
                    objects.append(obj.serialize())
        return objects

    def increase_w(self) -> None:
        self.w += self.BLOCK_SCALE
        if self.grid.divide(self.w) > self.grid.w - 1:
            self.grid.add_x()
        self.camera.reset(self.w, self.h)
        self.map_scrolling.reset(self.w, self.h)

    def increase_h(self) -> None:
        self.h += self.BLOCK_SCALE
        if self.grid.divide(self.h) > self.grid.h - 1:
            self.grid.add_y()
        self.camera.reset(self.w, self.h)
        self.map_scrolling.reset(self.w, self.h)

    def decrease_w(self) -> None:
        self.w -= self.BLOCK_SCALE
        if self.grid.w - 1 > self.grid.divide(self.w):
            self.grid.del_x()
        self.camera.reset(self.w, self.h)
        self.map_scrolling.reset(self.w, self.h)

    def decrease_h(self) -> None:
        self.h -= self.BLOCK_SCALE
        if self.grid.h - 1 > self.grid.divide(self.h):
            self.grid.del_y()
        self.camera.reset(self.w, self.h)
        self.map_scrolling.reset(self.w, self.h)


class Camera(BaseCamera):

    def get_cursor(self) -> XYTupleType:
        mouse_x_y: XYTupleType = get_pos()
        rect: Rect = self.rect.move(*mouse_x_y)
        return rect.x, rect.y


class Grid(BaseGrid):

    def __init__(self) -> None:
        super().__init__()
        self.camera: Camera = Camera()

    def add(self, object_: SomeEditorMapObjectType) -> None:
        y: int = self.divide(object_.rect.y)
        x: int = self.divide(object_.rect.x)
        if y < 0:
            y = 0
        elif y > self.h - 1:
            y = self.h - 1
        if x < 0:
            x = 0
        elif x > self.w - 1:
            x = self.w - 1
        self[y][x].append(object_)
        object_.grid_x_list = self[y][x]

    def add_x(self) -> None:
        for y in self:
            y.append([])

    def del_x(self) -> None:
        for y in self:
            del y[-1]

    def add_y(self) -> None:
        self.append([])
        for _ in range(self.w):
            self[-1].append([])

    def del_y(self) -> None:
        del self[-1]
