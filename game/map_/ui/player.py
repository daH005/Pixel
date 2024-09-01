from pygame import (
    K_LEFT, 
    K_RIGHT, 
    K_UP, 
    K_DOWN,
    K_w,
    K_a,
    K_d,
    K_SPACE,
    K_s,
)
from pygame.key import get_pressed, ScancodeWrapper

from engine.common.counters import FramesCounter, TimeCounter, calc_count_by_fps_from_seconds
from engine.common.float_rect import FloatRect
from engine.map_.map_ import Map
from game.assets.images import PlayerDefaultImages, PlayerDefaultWhiteImages
from game.assets.sounds import hit_sound
from game.map_.attrs import MapObjectAttr
from game.map_.abstract_ui import AbstractMovingMapObject, AbstractBlock

__all__ = (
    'Player',
)


@Map.add_object_type
class Player(AbstractMovingMapObject):

    _Z_INDEX: int = 5
    _MAX_HP: int = 3
    _SPEED: float = 5
    _GRAVITY: float = 0.5
    _JUMP_POWER: float = 11
    _X_PUSHING_DECELERATION: float = 1

    _GO_LEFT_KEYS = [K_LEFT, K_a]
    _GO_RIGHT_KEYS = [K_RIGHT, K_d]
    _JUMP_KEYS = [K_UP, K_w, K_SPACE]
    _GO_TOP_KEYS = [K_UP, K_w, K_SPACE]
    _GO_BOTTOM_KEYS = [K_DOWN, K_s]

    _pressed: ScancodeWrapper

    def __init__(self, map_: Map,
                 x: int, y: int,
                 ) -> None:
        super().__init__(
            map_=map_,
            rect=FloatRect(PlayerDefaultImages.STAND.get_rect(x=x, y=y)),
            z_index=self._Z_INDEX,
        )

        self._be_white_count: float = calc_count_by_fps_from_seconds(0.25)
        self._go_frames_counter: FramesCounter = FramesCounter(
            frames_count=len(PlayerDefaultImages.GO_RIGHT),
            transition_delay_as_seconds=0.1,
        )
        self._go_vertical_frames_counter: FramesCounter = FramesCounter(
            frames_count=len(PlayerDefaultImages.GO_VERTICAL),
            transition_delay_as_seconds=0.1,
        )
        self._god_mode_time_counter: TimeCounter = TimeCounter(1.2)
        self._flashing_time_counter: TimeCounter = TimeCounter(0.1)

        self._flashing_flag: bool = False
        self._on_ground: bool = False
        self._on_ladder: bool = False
        self._in_water: bool = False
        self._hp: int = self._MAX_HP
        self._has_shield: bool = False
        self._x_pushing: int = 0
        self._x_vel: float = 0
        self._y_vel: float = 0

    @property
    def hp(self) -> int:
        return self._hp

    @property
    def max_hp(self) -> int:
        return self._MAX_HP

    @property
    def has_shield(self) -> bool:
        return self._has_shield

    @property
    def x_vel(self) -> float:
        return self._x_vel

    @property
    def y_vel(self) -> float:
        return self._y_vel

    def update(self) -> None:
        self._pressed = get_pressed()
        super().update()
        self._on_ladder = False
        self._in_water = False

    def _move(self) -> None:
        self._update_x_vel()
        self._update_y_vel()
        self._update_rect_xy()

        if self._rect.y > self._map.levels_manager.current_level.h:
            self._hp = 0

    def _update_x_vel(self) -> None:
        if self._x_pushing:
            self._decrease_x_pushing()
            self._x_vel = self._x_pushing
        else:
            self._x_vel = 0
            if self._is_pressed(self._GO_LEFT_KEYS) and not self._is_pressed(self._GO_RIGHT_KEYS):
                self._x_vel = -self._SPEED
            elif self._is_pressed(self._GO_RIGHT_KEYS) and not self._is_pressed(self._GO_LEFT_KEYS):
                self._x_vel = self._SPEED
            if self._on_ladder or self._in_water:
                self._x_vel /= 1.5

    def _decrease_x_pushing(self) -> None:
        if self._x_pushing > 0:
            self._x_pushing -= self._X_PUSHING_DECELERATION
            if self._x_pushing < 0 or self._check_left_map_edge():
                self._x_pushing = 0
        elif self._x_pushing < 0:
            self._x_pushing += self._X_PUSHING_DECELERATION
            if self._x_pushing > 0 or self._check_right_map_edge():
                self._x_pushing = 0

    def _check_left_map_edge(self) -> None:
        if self._rect.left <= 0:
            self._rect.left = 0

    def _check_right_map_edge(self) -> None:
        if self._rect.right >= self._map.levels_manager.current_level.w:
            self._rect.right = self._map.levels_manager.current_level.w

    def _update_y_vel(self) -> None:
        if self._on_ladder or self._in_water:
            self._y_vel = 0
            if self._is_pressed(self._GO_TOP_KEYS) or self._is_pressed(self._JUMP_KEYS):
                self._y_vel = -self._SPEED
            elif self._on_ladder and self._is_pressed(self._GO_BOTTOM_KEYS):
                self._y_vel = self._SPEED
            elif self._in_water:
                self._y_vel = self._SPEED / 1.5
        else:
            if self._is_pressed(self._JUMP_KEYS) and self._on_ground:
                self._y_vel = -self._JUMP_POWER
            self._y_vel += self._GRAVITY
        self._on_ground = False

    def _update_rect_xy(self) -> None:
        blocks: list[AbstractBlock] = self._map.grid.visible_by_attrs([MapObjectAttr.BLOCK])

        self._rect.float_x += self._x_vel
        self._check_collision_with_blocks(blocks, self._x_vel, 0)
        self._check_left_map_edge()
        self._check_right_map_edge()

        self._rect.float_y += self._y_vel
        self._check_collision_with_blocks(blocks, 0, self._y_vel)

    def _check_collision_with_blocks(self, blocks: list[AbstractBlock],
                                     x_vel: float,
                                     y_vel: float,
                                     ) -> None:
        for block in blocks:
            self._check_collision_with_block(block, x_vel, y_vel)

    def _check_collision_with_block(self, block: AbstractBlock,
                                    x_vel: float,
                                    y_vel: float,
                                    ) -> None:
        if self._rect.colliderect(block._rect):
            if x_vel > 0:
                self._rect.right = block._rect.left
            elif x_vel < 0:
                self._rect.left = block._rect.right
            elif y_vel > 0:
                self._rect.bottom = block._rect.top
                self._y_vel = 0
                self._on_ground = True
            elif y_vel < 0:
                self._rect.top = block._rect.bottom
                self._y_vel = 0

    def hit(self, x_pushing: float | None = None,
            y_pushing: float | None = None,
            enemy_center_x: int | None = None,
            ) -> None:
        if not self._god_mode_time_counter.is_working():
            self._god_mode_time_counter.restart()
            if self._has_shield:
                self._has_shield = False
            else:
                self._hp -= 1
            hit_sound.play()
        if y_pushing is not None:
            self._y_vel = -y_pushing
        if x_pushing is not None and enemy_center_x is not None:
            if self._rect.centerx < enemy_center_x:
                self._x_pushing = -x_pushing
            elif self._rect.centerx > enemy_center_x:
                self._x_pushing = x_pushing

    def replenish_hp(self, hp_to_add: int = 1) -> None:
        self._hp += hp_to_add
        if self._hp > self._MAX_HP:
            self._hp = self._MAX_HP

    def _update_image(self) -> None:
        if self._god_mode_time_counter.delta() <= self._be_white_count:
            images = PlayerDefaultWhiteImages
        else:
            images = PlayerDefaultImages

        if self._x_pushing:
            if self._x_pushing > 0:
                self._image = images.GO_LEFT[self._go_frames_counter.current_index]
            elif self._x_pushing < 0:
                self._image = images.GO_RIGHT[self._go_frames_counter.current_index]
        elif self._on_ladder or (self._in_water and self._y_vel < 0):
            self._image = images.GO_VERTICAL[self._go_vertical_frames_counter.current_index]
            if self._y_vel:
                self._go_vertical_frames_counter.next()
        else:
            if self._x_vel < 0:
                self._image = images.GO_LEFT[self._go_frames_counter.current_index]
            elif self._x_vel > 0:
                self._image = images.GO_RIGHT[self._go_frames_counter.current_index]
            else:
                self._image = images.STAND
            self._go_frames_counter.next()

        self._god_mode_time_counter.next()
        if self._god_mode_time_counter.is_working():
            self._flashing_time_counter.next()

    def _draw(self) -> None:
        if not self._god_mode_time_counter.is_working():
            super()._draw()
        else:
            if not self._flashing_time_counter.is_working():
                self._flashing_flag = not self._flashing_flag
                self._flashing_time_counter.restart()
            if self._flashing_flag:
                super()._draw()
    
    def _is_pressed(self, keys: list[int]) -> bool:
        for key in keys:
            if self._pressed[key]:
                return True
        return False

    def in_god_mode(self) -> bool:
        return self._god_mode_time_counter.is_working()

    def jump_from_slug(self, y_vel: float) -> None:
        self._y_vel = y_vel

    def set_that_in_water(self) -> None:
        self._in_water = True

    def set_that_on_ladder(self) -> None:
        self._on_ladder = True

    def add_shield(self) -> None:
        self._has_shield = True
