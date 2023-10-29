from pygame import Rect

from game.contrib.singleton_ import SingletonMeta
from game.contrib.screen import SCREEN_SIZE
from game.contrib.rects import FloatRect

__all__ = (
    'Camera',
)


class Camera(metaclass=SingletonMeta):
    SMOOTH = 0.05
    rect: FloatRect = FloatRect((0, 0) + SCREEN_SIZE)
    central_rect: Rect
    map_w: int
    map_h: int

    def __init__(self) -> None:
        self.x_to_move: int = 0
        self.y_to_move: int = 0

    def reset(self, map_w: int, map_h: int) -> None:
        self.map_w: int = map_w
        self.map_h: int = map_h

    def update(self) -> None:
        self._update_coords_to_move()
        self._update_float_coords()

    def _update_coords_to_move(self) -> None:
        self.x_to_move = -self.central_rect.centerx + self.rect.w // 2
        self.y_to_move = -self.central_rect.centery + self.rect.h // 2
        self._consider_map_edges()

    def _consider_map_edges(self) -> None:
        self.x_to_move = min(0, self.x_to_move)
        self.x_to_move = max(-(self.map_w - self.rect.w), self.x_to_move)
        self.y_to_move = min(0, self.y_to_move)
        self.y_to_move = max(-(self.map_h - self.rect.h), self.y_to_move)

    def _update_float_coords(self) -> None:
        self.rect.float_x += (-self.x_to_move - self.rect.float_x) * self.SMOOTH
        self.rect.float_y += (-self.y_to_move - self.rect.float_y) * self.SMOOTH

    def move_quick(self) -> None:
        self._update_coords_to_move()
        self._update_float_coords_quick()

    def _update_float_coords_quick(self) -> None:
        self.rect.float_x = -self.x_to_move
        self.rect.float_y = -self.y_to_move

    def apply(self, rect: Rect | FloatRect) -> Rect:
        return rect.move(-self.rect.x, -self.rect.y)
