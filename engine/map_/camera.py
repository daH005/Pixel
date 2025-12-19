from pygame import Rect

from engine.common.singleton import SingletonMeta
from engine.common.float_rect import FloatRect
from engine.common.typing_ import SizeTupleType, AnyRectType, XYTupleType, CameraBoundingLinesType
from engine.screen_access_mixin import ScreenAccessMixin

__all__ = (
    'Camera',
)


class Camera(ScreenAccessMixin, metaclass=SingletonMeta):

    _map_w: int
    _map_h: int
    _bounding_horizontal_lines: CameraBoundingLinesType
    _central_rect: Rect

    def __init__(self, x_smooth: float = 0.05,
                 y_smooth: float = 0.01,
                 ) -> None:
        self._x_smooth = x_smooth
        self._y_smooth = y_smooth

        self._screen_size: SizeTupleType = self._screen.get_size()
        self._rect: FloatRect = FloatRect(
            (0, 0) + self._screen_size
        )
        self._x_to_move: int = 0
        self._y_to_move: int = 0
        self._central_x: int = 0
        self._central_y: int = 0

    @property
    def float_x(self) -> float:
        return self._rect.float_x

    def reset(self, map_w: int,
              map_h: int,
              camera_bounding_horizontal_lines: CameraBoundingLinesType | None = None,
              ) -> None:
        if camera_bounding_horizontal_lines is None:
            camera_bounding_horizontal_lines = []

        self._map_w = map_w
        self._map_h = map_h
        self._bounding_horizontal_lines = camera_bounding_horizontal_lines

    def update(self, central_rect: Rect) -> None:
        self._central_rect = central_rect
        self._update_xy_to_move()
        self._update_float_xy()

    def _update_xy_to_move(self) -> None:
        self._x_to_move = self._central_rect.centerx - self._rect.w // 2
        self._y_to_move = self._central_rect.centery - self._rect.h // 2
        self._consider_map_edges()

    def _consider_map_edges(self) -> None:
        self._x_to_move = max(0, self._x_to_move)
        self._x_to_move = min(self._map_w - self._rect.w, self._x_to_move)
        self._y_to_move = max(0, self._y_to_move)
        self._y_to_move = min(self._define_bounding_bottom_y(), self._y_to_move)

    def _define_bounding_bottom_y(self) -> int:
        for line in self._bounding_horizontal_lines:
            if not (self._rect.left >= line[0] and self._rect.right <= line[1]):
                continue
            return line[2] - self._rect.h
        return self._map_h - self._rect.h

    def _update_float_xy(self) -> None:
        x_vel = (self._x_to_move - self._rect.float_x) * self._x_smooth
        y_vel = (self._y_to_move - self._rect.float_y) * self._y_smooth
        self._rect.float_x += x_vel
        self._rect.float_y += y_vel

    def move_quick(self, central_rect: Rect) -> None:
        self._central_rect = central_rect
        self._update_xy_to_move()
        self._update_float_xy_quick()

    def _update_float_xy_quick(self) -> None:
        self._rect.float_x = self._x_to_move
        self._rect.float_y = self._y_to_move

    def apply_rect(self, rect: AnyRectType) -> AnyRectType:
        rect = rect.copy()
        rect.x -= self._rect.x
        rect.y -= self._rect.y
        return rect

    def apply_xy(self, xy: XYTupleType) -> XYTupleType:
        return xy[0] - self._rect.x, xy[1] - self._rect.y

    @property
    def centerx(self) -> int:
        return self._rect.centerx

    @property
    def centery(self) -> int:
        return self._rect.centery
