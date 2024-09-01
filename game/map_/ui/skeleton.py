from pygame import Rect

from engine.map_.map_ import Map
from engine.common.counters import FramesCounter
from engine.common.direction import Direction
from engine.common.float_rect import FloatRect
from game.assets.images import SkeletonImages
from game.map_.abstract_ui import AbstractXPatrolEnemy

__all__ = (
    'Skeleton',
)


@Map.add_object_type
class Skeleton(AbstractXPatrolEnemy):

    _SPEED: float = 1.5
    _X_PUSHING_POWER: float = 20
    _Y_PUSHING_POWER: float = 3
    _ATTACK_ANIM_INDENTS: dict[Direction, tuple[int, int]] = {
        Direction.LEFT: (0, 72),
        Direction.RIGHT: (28, 0),
    }
    _ATTACK_FRAME_INDEX: int = 1

    def __init__(self, map_: Map,
                 x: int, y: int,
                 start_x: int,
                 end_x: int,
                 ) -> None:
        super().__init__(
            map_=map_,
            rect=FloatRect(SkeletonImages.GO_RIGHT[0].get_rect(x=x, y=y)),
            start_x=start_x,
            end_x=end_x,
            speed=self._SPEED,
            x_pushing_power=self._X_PUSHING_POWER,
            y_pushing_power=self._Y_PUSHING_POWER,
        )

        self._go_frames_counter: FramesCounter = FramesCounter(
            frames_count=len(SkeletonImages.GO_RIGHT),
            transition_delay_as_seconds=0.15,
        )
        self._attack_frames_counter: FramesCounter = FramesCounter(
            frames_count=len(SkeletonImages.ATTACK_RIGHT),
            transition_delay_as_seconds=0.15,
        )

        self._anim_rect: Rect = self._rect
        self.attack_direction: Direction | None = None

    def _move(self) -> None:
        if self._attack_frames_counter.is_end:
            super()._move()

    def _handle_collision_with_player(self) -> None:
        if self._attack_frames_counter.current_index == self._ATTACK_FRAME_INDEX:
            super()._handle_collision_with_player()
        if self._attack_frames_counter.is_end:
            self._attack_frames_counter.start()
            if self._map.player.get_rect().centerx < self._rect.centerx:
                self.attack_direction = Direction.LEFT
            elif self._map.player.get_rect().centerx >= self._rect.centerx:
                self.attack_direction = Direction.RIGHT

    def _update_image(self) -> None:
        if self._attack_frames_counter.is_end:
            self._anim_rect = self._rect
            if self._x_vel < 0:
                self._image = SkeletonImages.GO_LEFT[self._go_frames_counter.current_index]
            elif self._x_vel > 0:
                self._image = SkeletonImages.GO_RIGHT[self._go_frames_counter.current_index]
            self._go_frames_counter.next()
        else:
            if self.attack_direction == Direction.LEFT:
                self._image = SkeletonImages.ATTACK_LEFT[self._attack_frames_counter.current_index]
            elif self.attack_direction == Direction.RIGHT:
                self._image = SkeletonImages.ATTACK_RIGHT[self._attack_frames_counter.current_index]
            self._update_anim_rect_for_attack()
            self._attack_frames_counter.next()

    def _update_anim_rect_for_attack(self) -> None:
        self._anim_rect = Rect(
            self._rect.x - self._ATTACK_ANIM_INDENTS[self.attack_direction][self._attack_frames_counter.current_index],
            0,
            self._image.get_width(),
            self._image.get_height(),
        )
        self._anim_rect.bottom = self._rect.bottom

    def _draw(self) -> None:
        self._screen.blit(self._image, self._map.camera.apply(self._anim_rect))
