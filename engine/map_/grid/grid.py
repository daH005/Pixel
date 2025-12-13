from math import ceil

from engine.common.singleton import SingletonMeta
from engine.map_.camera import Camera
from engine.map_.grid.abstract_grid_object import AnyGridObjectType
from engine.map_.grid.typing_ import RangesType
from engine.screen_access_mixin import ScreenAccessMixin

__all__ = (
    'Grid',
)


class Grid(ScreenAccessMixin, metaclass=SingletonMeta):

    def __init__(self, camera: Camera) -> None:
        super().__init__()
        self._camera = camera

        self._cell_side_len = self._screen.get_width()
        self._visible_objects: list[AnyGridObjectType] = []
        self._grid: list[list[list[AnyGridObjectType]]] = []

    @property
    def w(self) -> int:
        return len(self._grid[0])

    @property
    def h(self) -> int:
        return len(self._grid)

    @property
    def visible_objects(self) -> list[AnyGridObjectType]:
        return self._visible_objects

    def reset(self, map_w: int, map_h: int) -> None:
        self._grid.clear()
        self._build_cells(
            self._divide(map_w, ceil_=True),
            self._divide(map_h, ceil_=True),
        )

    def _build_cells(self, w: int, h: int) -> None:
        for _ in range(h):
            self._grid.append([])
            for _ in range(w):
                self._grid[-1].append([])

    def _divide(self, n: int, ceil_: bool = False) -> int:
        r: float = n / self._cell_side_len
        if ceil_:
            return ceil(r)
        return int(r)

    def add(self, object_: AnyGridObjectType) -> None:
        y: int = self._divide(object_.y)
        x: int = self._divide(object_.x)
        if y < 0:
            y = 0
        elif y > self.h - 1:
            y = self.h - 1
        if x < 0:
            x = 0
        elif x > self.w - 1:
            x = self.w - 1
        self._grid[y][x].append(object_)

    def update(self) -> None:
        ranges: RangesType = self._calc_ranges()
        self._visible_objects.clear()
        for cur_cell_y in range(*ranges[0]):
            for cur_cell_x in range(*ranges[1]):
                self._update_objects(self._grid[cur_cell_y][cur_cell_x])
        self._visible_objects = list(set(self._visible_objects))

    def _calc_ranges(self) -> RangesType:
        start_cell_x: int = self._divide(self._camera.centerx)
        start_cell_y: int = self._divide(self._camera.centery)
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

    def _update_objects(self, objects: list[AnyGridObjectType]) -> None:
        for object_ in objects[:]:
            objects.remove(object_)
            if not object_.to_delete:
                self.add(object_)
                self._visible_objects.append(object_)

    def visible_by_attrs(self, desired_attrs: list[int]) -> list[AnyGridObjectType]:
        desired_objects: list[AnyGridObjectType] = []
        for object_ in self._visible_objects:
            if self._attrs_is_exist(object_.grid_attrs, desired_attrs):
                desired_objects.append(object_)
        return desired_objects

    @staticmethod
    def _attrs_is_exist(attrs: list[int],
                        desired_attrs: list[int],
                        ) -> bool:
        for desired_attr in desired_attrs:
            if desired_attr not in attrs:
                return False
        return True
