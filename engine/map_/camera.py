from pygame import Rect

from engine.common.singleton import SingletonMeta
from engine.common.float_rect import FloatRect
from engine.common.typing_ import SizeTupleType
from engine.screen_access_mixin import ScreenAccessMixin

__all__ = (
    'Camera',
)


class Camera(ScreenAccessMixin, metaclass=SingletonMeta):
    _map_w: int
    _map_h: int
    _central_rect: Rect

    def __init__(self, smooth: float) -> None:
        self._smooth = smooth

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
              ) -> None:
        self._map_w = map_w
        self._map_h = map_h

    def update(self, central_rect: Rect) -> None:
        self._central_rect = central_rect
        self._update_xy_to_move()
        self._update_float_xy()

    def _update_xy_to_move(self) -> None:
        self._x_to_move = -self._central_rect.centerx + self._rect.w // 2
        self._y_to_move = -self._central_rect.centery + self._rect.h // 2
        self._consider_map_edges()

    def _consider_map_edges(self) -> None:
        self._x_to_move = min(0, self._x_to_move)
        self._x_to_move = max(-(self._map_w - self._rect.w), self._x_to_move)
        self._y_to_move = min(0, self._y_to_move)
        self._y_to_move = max(-(self._map_h - self._rect.h), self._y_to_move)

    def _update_float_xy(self) -> None:
        self._rect.float_x += (-self._x_to_move - self._rect.float_x) * self._smooth
        self._rect.float_y += (-self._y_to_move - self._rect.float_y) * self._smooth

    def move_quick(self, central_rect: Rect) -> None:
        self._central_rect = central_rect
        self._update_xy_to_move()
        self._update_float_xy_quick()

    def _update_float_xy_quick(self) -> None:
        self._rect.float_x = -self._x_to_move
        self._rect.float_y = -self._y_to_move

    def apply(self, rect: Rect | FloatRect) -> Rect:
        return rect.move(-self._rect.x, -self._rect.y)

    def get_rect(self):
        return self._rect.copy()
