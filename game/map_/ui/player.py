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
    Rect,
)
from pygame.key import get_pressed, ScancodeWrapper

from engine.common.counters import FramesCounter, TimeCounter, calc_count_by_fps_from_seconds
from engine.common.float_rect import FloatRect
from engine.map_.map_ import Map
from engine.map_.collision_checkable_mixin import CollisionCheckableMixin
from engine.common.direction import Direction
from game.assets.images import PlayerDefaultImages, PlayerDefaultWhiteImages
from game.assets.sounds import hit_sound
from game.map_.grid_attrs import GridObjectAttr
from game.map_.abstract_ui import AbstractMovingMapObject, AbstractBlock

__all__ = (
    'Player',
)


@Map.add_object_type
class Player(AbstractMovingMapObject, CollisionCheckableMixin):

    _Z_INDEX = 5
    _DEFAULT_IMAGES = PlayerDefaultImages
    _WHITE_IMAGES = PlayerDefaultWhiteImages

    _BE_WHITE_DURATION: float = 0.25
    _GOD_MOD_DURATION: float = 1.2
    _FLASHING_DURATION: float = 0.1
    _GO_ANIMATION_DELAY: float = 0.13
    _STAND_ANIMATION_DELAY: float = 2

    _MAX_HP: int = 3
    _SPEED: float = 5
    _GRAVITY: float = 0.5
    _JUMP_POWER: float = 11
    _X_PUSHING_DECELERATION: float = 1
    _WATER_OR_LADDER_VEL_DECREASE_FACTOR: float = 1.5
    _ABSOLUTE_Y_VEL_TO_FALLING_DETECTION: float = 1

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
            rect=FloatRect(self._DEFAULT_IMAGES.STAND_RIGHT[0].get_rect(x=x, y=y)),
        )
        self._map.set_player(self)

        self._be_white_count: float = calc_count_by_fps_from_seconds(self._BE_WHITE_DURATION)
        self._go_frames_counter: FramesCounter = FramesCounter(
            frames_count=len(self._DEFAULT_IMAGES.GO_RIGHT),
            transition_delay_as_seconds=self._GO_ANIMATION_DELAY,
        )
        self._stand_frames_counter: FramesCounter = FramesCounter(
            frames_count=len(self._DEFAULT_IMAGES.STAND_RIGHT),
            transition_delay_as_seconds=self._STAND_ANIMATION_DELAY,
        )
        self._go_vertical_frames_counter: FramesCounter = FramesCounter(
            frames_count=len(self._DEFAULT_IMAGES.GO_VERTICAL),
            transition_delay_as_seconds=self._GO_ANIMATION_DELAY,
        )
        self._god_mode_time_counter: TimeCounter = TimeCounter(self._GOD_MOD_DURATION)
        self._flashing_time_counter: TimeCounter = TimeCounter(self._FLASHING_DURATION)

        self._flashing_flag: bool = False
        self._on_ground: bool = False
        self._on_ladder: bool = False
        self._in_water: bool = False
        self._hp: int = self._MAX_HP
        self._has_shield: bool = False
        self._x_pushing: int = 0
        self._x_vel: float = 0
        self._y_vel: float = 0
        self._direction: Direction = Direction.RIGHT

    @property
    def hp(self) -> int:
        return self._hp

    @classmethod
    @property
    def max_hp(cls) -> int:
        return cls._MAX_HP

    @property
    def has_shield(self) -> bool:
        return self._has_shield

    @property
    def x_vel(self) -> float:
        return self._x_vel

    @property
    def y_vel(self) -> float:
        return self._y_vel

    @property
    def direction(self) -> Direction:
        return self._direction

    def update(self) -> None:
        self._pressed = get_pressed()
        super().update()
        self._on_ladder = False
        self._in_water = False

    def _move(self) -> None:
        self._set_on_ground_or_not()
        self._update_x_vel()
        self._update_y_vel()
        self._update_rect_xy()
        self._kill_if_is_out_of_map()

    def _set_on_ground_or_not(self) -> None:
        if abs(self._y_vel) >= self._ABSOLUTE_Y_VEL_TO_FALLING_DETECTION:
            self._on_ground = False

    def _update_x_vel(self) -> None:
        if self._x_pushing:
            self._decrease_x_pushing()
            self._x_vel = self._x_pushing
        else:
            self._x_vel = 0
            if self._is_pressed(self._GO_LEFT_KEYS) and not self._is_pressed(self._GO_RIGHT_KEYS):
                self._x_vel = -self._SPEED
                self._direction = Direction.LEFT
            elif self._is_pressed(self._GO_RIGHT_KEYS) and not self._is_pressed(self._GO_LEFT_KEYS):
                self._x_vel = self._SPEED
                self._direction = Direction.RIGHT
            if self._on_ladder or self._in_water:
                self._x_vel /= self._WATER_OR_LADDER_VEL_DECREASE_FACTOR

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
                self._y_vel = self._SPEED / self._WATER_OR_LADDER_VEL_DECREASE_FACTOR
        else:
            if self._is_pressed(self._JUMP_KEYS) and self._on_ground:
                self._y_vel = -self._JUMP_POWER
            self._y_vel += self._GRAVITY

    def _update_rect_xy(self) -> None:
        blocks: list[AbstractBlock] = self._map.grid.visible_by_attrs([GridObjectAttr.BLOCK])

        self._rect.float_x += self._x_vel
        self._handle_collision_with_blocks(blocks, self._x_vel, 0)
        self._check_left_map_edge()
        self._check_right_map_edge()

        self._rect.float_y += self._y_vel
        self._handle_collision_with_blocks(blocks, 0, self._y_vel)

    def _handle_collision_with_blocks(self, blocks: list[AbstractBlock],
                                      x_vel: float,
                                      y_vel: float,
                                      ) -> None:
        for block in blocks:
            self._handle_collision_with_bounding_rect(block.get_rect(), x_vel, y_vel)

    def _handle_bottom_collision(self, block_rect: Rect) -> None:
        super()._handle_bottom_collision(block_rect)
        self._on_ground = True

    def _kill_if_is_out_of_map(self) -> None:
        if self._rect.y > self._map.levels_manager.current_level.h:
            self._hp = 0

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
            images = self._WHITE_IMAGES
        else:
            images = self._DEFAULT_IMAGES

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
            if self._direction == Direction.LEFT:
                if self._x_vel < 0:
                    self._image = images.GO_LEFT[self._go_frames_counter.current_index]
                elif not self._on_ground:
                    self._image = images.GO_LEFT[0]
                else:
                    self._image = images.STAND_LEFT[self._stand_frames_counter.current_index]
            elif self._direction == Direction.RIGHT:
                if self._x_vel > 0:
                    self._image = images.GO_RIGHT[self._go_frames_counter.current_index]
                elif not self._on_ground:
                    self._image = images.GO_RIGHT[0]
                else:
                    self._image = images.STAND_RIGHT[self._stand_frames_counter.current_index]

            self._go_frames_counter.next()
            self._stand_frames_counter.next()

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
