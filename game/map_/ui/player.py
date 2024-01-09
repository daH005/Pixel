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

from game.assets.images import PlayerDefaultImages, PlayerDefaultWhiteImages
from game.assets.sounds import hit_sound
from game.contrib.counters import FramesCounter, TimeCounter, calc_count_by_fps_from_seconds
from game.contrib.annotations import SizeTupleType
from game.contrib.rects import FloatRect
from game.map_.map_ import Map
from game.map_.grid import MapObjectAttr
from game.map_.abstract_ui import AbstractMovingMapObject, AbstractBlock

__all__ = (
    'Player',
)


@Map.add_object_type
class Player(AbstractMovingMapObject):
    size: SizeTupleType = PlayerDefaultImages.STAND.get_size()
    Z_INDEX: int = 5
    RectType: FloatRect = FloatRect

    MAX_HP: int = 3
    SPEED: float = 5
    JUMP_POWER: float = 11
    GRAVITY: float = 0.5

    GO_LEFT_KEYS: list[int] = [K_LEFT, K_a]
    GO_RIGHT_KEYS: list[int] = [K_RIGHT, K_d]
    JUMP_KEYS: list[int] = [K_UP, K_w, K_SPACE]
    GO_TOP_KEYS: list[int] = [K_UP, K_w, K_SPACE]
    GO_BOTTOM_KEYS: list[int] = [K_DOWN, K_s]

    GO_ANIM_DELAY: float = 0.1
    LADDER_ANIM_DELAY: float = 0.1
    GOD_MOD_DURATION: float = 1.2
    BE_WHITE_COUNT: float = calc_count_by_fps_from_seconds(0.25)
    FLASHING_INTERVAL: float = 0.1
    X_PUSHING_DECELERATION: float = 1

    pressed: ScancodeWrapper

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.map.player = self

        self.go_frames_counter: FramesCounter = FramesCounter(
            frames_count=len(PlayerDefaultImages.GO_LEFT),
            transition_delay_as_seconds=self.GO_ANIM_DELAY,
        )
        self.ladder_frames_counter: FramesCounter = FramesCounter(
            frames_count=len(PlayerDefaultImages.LADDER),
            transition_delay_as_seconds=self.LADDER_ANIM_DELAY,
        )
        self.god_mode_time_counter: TimeCounter = TimeCounter(self.GOD_MOD_DURATION)
        self.flashing_time_counter: TimeCounter = TimeCounter(self.FLASHING_INTERVAL)

        self.flashing_flag: bool = False
        self.on_ground: bool = False
        self.on_ladder: bool = False
        self.in_water: bool = False
        self.hp: int = self.MAX_HP
        self.has_shield: bool = False
        self.x_pushing: int = 0
        self.x_vel: float = 0
        self.y_vel: float = 0

    def update(self) -> None:
        self.pressed = get_pressed()
        super().update()
        # Этот флаг может стать `True` в `Ladder._handler_collision_with_player(...)`.
        self.on_ladder = False
        # Этот флаг может стать `True` в `Water._handler_collision_with_player(...)`.
        self.in_water = False

    def _move(self) -> None:
        self._update_x_vel()
        self._update_y_vel()
        self._update_rect_xy()
        # Убиваем персонажа, если он выпал за нижний край карты.
        if self.rect.y > self.map.level.h:
            self.hp = 0

    def _update_x_vel(self) -> None:
        if self.x_pushing:
            self._decrease_x_pushing()
            self.x_vel = self.x_pushing
        else:
            self.x_vel = 0
            if self._is_pressed(self.GO_LEFT_KEYS) and not self._is_pressed(self.GO_RIGHT_KEYS):
                self.x_vel = -self.SPEED
            elif self._is_pressed(self.GO_RIGHT_KEYS) and not self._is_pressed(self.GO_LEFT_KEYS):
                self.x_vel = self.SPEED
            if self.on_ladder or self.in_water:
                self.x_vel /= 1.5

    def _decrease_x_pushing(self) -> None:
        if self.x_pushing > 0:
            self.x_pushing -= self.X_PUSHING_DECELERATION
            if self.x_pushing < 0 or self._check_left_map_edge():
                self.x_pushing = 0
        elif self.x_pushing < 0:
            self.x_pushing += self.X_PUSHING_DECELERATION
            if self.x_pushing > 0 or self._check_right_map_edge():
                self.x_pushing = 0

    def _check_left_map_edge(self) -> None:
        if self.rect.left <= 0:
            self.rect.left = 0

    def _check_right_map_edge(self) -> None:
        if self.rect.right >= self.map.level.w:
            self.rect.right = self.map.level.w

    def _update_y_vel(self) -> None:
        if self.on_ladder or self.in_water:
            self.y_vel = 0
            if self._is_pressed(self.GO_TOP_KEYS) or self._is_pressed(self.JUMP_KEYS):
                self.y_vel = -self.SPEED
            elif self.on_ladder and self._is_pressed(self.GO_BOTTOM_KEYS):
                self.y_vel = self.SPEED
            elif self.in_water:
                self.y_vel = self.SPEED / 1.5
        else:
            if self._is_pressed(self.JUMP_KEYS) and self.on_ground:
                self.y_vel = -self.JUMP_POWER
            self.y_vel += self.GRAVITY
        self.on_ground = False

    def _update_rect_xy(self) -> None:
        blocks: list[AbstractBlock] = self.map.grid.visible_by_attrs([MapObjectAttr.BLOCK])
        # Смотрим по Х:
        self.rect.float_x += self.x_vel
        self._check_collision_with_blocks(blocks, self.x_vel, 0)
        self._check_left_map_edge()
        self._check_right_map_edge()
        # Смотрим по У:
        self.rect.float_y += self.y_vel
        self._check_collision_with_blocks(blocks, 0, self.y_vel)

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
        if self.rect.colliderect(block.rect):
            if x_vel > 0:
                self.rect.right = block.rect.left
            elif x_vel < 0:
                self.rect.left = block.rect.right
            elif y_vel > 0:
                self.rect.bottom = block.rect.top
                self.y_vel = 0
                self.on_ground = True
            elif y_vel < 0:
                self.rect.top = block.rect.bottom
                self.y_vel = 0

    def hit(self, x_pushing: float | None = None,
            y_pushing: float | None = None,
            enemy_center_x: int | None = None,
            ) -> None:
        if not self.god_mode_time_counter.is_work():
            self.god_mode_time_counter.restart()
            if self.has_shield:
                self.has_shield = False
            else:
                self.hp -= 1
            hit_sound.play()
        if y_pushing is not None:
            self.y_vel = -y_pushing
        if x_pushing is not None and enemy_center_x is not None:
            if self.rect.centerx < enemy_center_x:
                self.x_pushing = -x_pushing
            elif self.rect.centerx > enemy_center_x:
                self.x_pushing = x_pushing

    def relpenish_hp(self, addition: int = 1) -> None:
        self.hp += addition
        if self.hp > self.MAX_HP:
            self.hp = self.MAX_HP

    def _update_image(self) -> None:
        if self.god_mode_time_counter.delta() <= self.BE_WHITE_COUNT:
            # На пару мгновений будем красить персонажа в белый для визуального обозначения урона.
            images = PlayerDefaultWhiteImages
        else:
            images = PlayerDefaultImages

        if self.x_pushing:
            # При толчке персонаж замирает и поворачивается в сторону противоположной
            # стороне полёта.
            if self.x_pushing > 0:
                self.image = images.GO_LEFT[self.go_frames_counter.current_index]
            elif self.x_pushing < 0:
                self.image = images.GO_RIGHT[self.go_frames_counter.current_index]
        elif self.on_ladder or (self.in_water and self.y_vel < 0):
            self.image = images.LADDER[self.ladder_frames_counter.current_index]
            if self.y_vel:
                self.ladder_frames_counter.next()
        else:
            if self.x_vel < 0:
                self.image = images.GO_LEFT[self.go_frames_counter.current_index]
            elif self.x_vel > 0:
                self.image = images.GO_RIGHT[self.go_frames_counter.current_index]
            else:
                self.image = images.STAND
            self.go_frames_counter.next()

        self.god_mode_time_counter.next()
        if self.god_mode_time_counter.is_work():
            self.flashing_time_counter.next()

    def _draw(self) -> None:
        if not self.god_mode_time_counter.is_work():
            super()._draw()
        else:
            if not self.flashing_time_counter.is_work():
                self.flashing_flag = not self.flashing_flag
                self.flashing_time_counter.restart()
            if self.flashing_flag:
                super()._draw()
    
    def _is_pressed(self, keys: list[int]) -> bool:
        for key in keys:
            if self.pressed[key]:
                return True
        return False
    