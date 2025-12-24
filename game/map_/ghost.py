from pygame import Rect

from engine.map_.map_ import Map
from engine.common.float_rect import FloatRect
from game.assets.images import GhostImages
from game.map_.abstract_ui import AbstractXPatrolEnemy

__all__ = (
    'Ghost',
)


@Map.add_object_type
class Ghost(AbstractXPatrolEnemy):

    _SPEED = 0.5
    _ATTACK_SPEED: float = 3
    _X_PUSHING_POWER = 5
    _Y_PUSHING_POWER = 5

    _IMAGES = GhostImages
    _Y_DEVIATION: int = 5
    _Y_DEVIATION_SPEED: float = 0.1

    def __init__(self, map_: Map,
                 x: int, y: int,
                 start_x: int,
                 end_x: int,
                 ) -> None:
        super().__init__(
            map_=map_,
            rect=FloatRect(self._IMAGES.GO_RIGHT.get_rect(x=x, y=y)),
            start_x=start_x,
            end_x=end_x,
        )
        self._reaction_rect: Rect = Rect(self._start_x, self._rect.y, self._end_x - self._start_x, self._rect.h)

        self._y_at_top: int = self._rect.y - self._Y_DEVIATION
        self._y_at_bottom: int = self._rect.y + self._Y_DEVIATION
        self._current_y_deviation_vel: float = self._Y_DEVIATION_SPEED

        self._is_in_attack_mode: bool = False
        self._direction_factor_backup: int = 1

    def update(self) -> None:
        self._handle_collision_reaction_rect_with_player()
        super().update()

    def _handle_collision_reaction_rect_with_player(self) -> None:
        if self._reaction_rect.colliderect(self._map.player.get_rect()):
            if not self._is_in_attack_mode:
                self._direction_factor_backup = 1 if self._x_vel > 0 else -1
            self._is_in_attack_mode = True
        else:
            if self._is_in_attack_mode:
                self._x_vel = self._SPEED * self._direction_factor_backup
            self._is_in_attack_mode = False

    def _move(self) -> None:
        self._set_x_vel_direction_regarding_player_pos()
        super()._move()
        self._do_y_deviation()

    def _set_x_vel_direction_regarding_player_pos(self) -> None:
        if self._is_in_attack_mode:
            if self._map.player.get_rect().centerx >= self._rect.centerx:
                self._x_vel = self._ATTACK_SPEED
            else:
                self._x_vel = -self._ATTACK_SPEED

    def _do_y_deviation(self) -> None:
        self._rect.float_y += self._current_y_deviation_vel
        if self._rect.y <= self._y_at_top or self._rect.y >= self._y_at_bottom:
            self._current_y_deviation_vel *= -1

    def _update_image(self) -> None:
        if self._x_vel > 0:
            if self._is_in_attack_mode:
                self._image = self._IMAGES.ATTACK_RIGHT
            else:
                self._image = self._IMAGES.GO_RIGHT
        elif self._x_vel < 0:
            if self._is_in_attack_mode:
                self._image = self._IMAGES.ATTACK_LEFT
            else:
                self._image = self._IMAGES.GO_LEFT
