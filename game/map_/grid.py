from enum import IntEnum
from abc import ABC
from typing import TypeVar, TypeAlias
from math import ceil

from game.contrib.singleton_ import SingletonMeta
from game.contrib.abstract_ui import AbstractUI
from game.map_.camera import Camera
from game.contrib.screen import SCREEN_W

__all__ = (
    'AbstractMapGridObject',
    'SomeMapObjectType',
    'MapObjectAttr',
    'MapObjectAttrsListType',
    'RangesType',
    'Grid',
)


class MapObjectAttr(IntEnum):
    BLOCK = 0
    PLAYER = 1
    SLUG = 2


MapObjectAttrsListType: TypeAlias = list[MapObjectAttr]
RangesType: TypeAlias = tuple[tuple[int, int], tuple[int, int]]


class AbstractMapGridObject(AbstractUI, ABC):
    ATTRS: list[MapObjectAttr]
    to_delete: bool


SomeMapObjectType: TypeVar = TypeVar('SomeMapObjectType', bound=AbstractMapGridObject, covariant=True)


class Grid(list, metaclass=SingletonMeta):
    CELL_SCALE: int = SCREEN_W

    def __init__(self) -> None:
        super().__init__()
        self.camera: Camera = Camera()
        self.visible_objects: list[SomeMapObjectType] = []

    @property
    def w(self) -> int:
        return len(self[0])

    @property
    def h(self) -> int:
        return len(self)

    def reset(self, map_w: int, map_h: int) -> None:
        self.clear()
        self._build_cells(
            self.divide(map_w, ceil_=True),
            self.divide(map_h, ceil_=True),
        )

    def _build_cells(self, w: int, h: int) -> None:
        for _ in range(h):
            self.append([])
            for _ in range(w):
                self[-1].append([])

    def divide(self, n: int, ceil_: bool = False) -> int:
        r: float = n / self.CELL_SCALE
        if ceil_:
            return ceil(r)
        return int(r)

    def add(self, object_: SomeMapObjectType) -> None:
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

    def update(self) -> None:
        ranges: RangesType = self._calc_ranges()
        self.visible_objects.clear()
        for cur_cell_y in range(*ranges[0]):
            for cur_cell_x in range(*ranges[1]):
                self._update_objects(self[cur_cell_y][cur_cell_x])
        self.visible_objects = list(set(self.visible_objects))

    def _calc_ranges(self) -> RangesType:
        start_cell_x: int = self.divide(self.camera.rect.centerx)
        start_cell_y: int = self.divide(self.camera.rect.centery)
        end_cell_x: int = start_cell_x
        end_cell_y: int = start_cell_y
        if start_cell_x != 0:
            start_cell_x -= 1
        if start_cell_y != 0:
            start_cell_y -= 1
        if end_cell_x != self.w - 1:
            end_cell_x += 1
        if end_cell_y != self.h - 1:
            end_cell_y += 1
        return (start_cell_y, end_cell_y + 1), (start_cell_x, end_cell_x + 1)

    def _update_objects(self, objects: list[SomeMapObjectType]) -> None:
        for object_ in objects[:]:
            objects.remove(object_)
            if not object_.to_delete:
                self.add(object_)
                self.visible_objects.append(object_)

    def visible_by_attrs(self, desired_attrs: list[MapObjectAttr]) -> list[SomeMapObjectType]:
        desired_objects: list[SomeMapObjectType] = []
        for object_ in self.visible_objects:
            if self._attrs_is_exist(object_.ATTRS, desired_attrs):
                desired_objects.append(object_)
        return desired_objects

    @staticmethod
    def _attrs_is_exist(attrs: list[MapObjectAttr],
                        desired_attrs: list[MapObjectAttr],
                        ) -> bool:
        for desired_attr in desired_attrs:
            if desired_attr not in attrs:
                return False
        return True
