from pygame import Rect

from game.assets.images import SkeletonImages
from game.contrib.counters import FramesCounter
from game.contrib.annotations import SizeTupleType
from game.contrib.direction import Direction
from game.map_.map_ import Map
from game.map_.abstract_ui import AbstractXPatrolEnemy
from game.contrib.screen import screen

__all__ = (
    'Skeleton',
)


@Map.add_object_type
class Skeleton(AbstractXPatrolEnemy):
    size: SizeTupleType = SkeletonImages.GO_RIGHT[0].get_size()
    SPEED: float = 1.5
    X_PUSHING_POWER: float = 20
    Y_PUSHING_POWER: float = 3

    GO_ANIM_DELAY: float = 0.15
    ATTACK_ANIM_DELAY: float = 0.15
    ATTACK_ANIM_INDENTS: dict[Direction, tuple[int, int]] = {
        Direction.LEFT: (0, 72),
        Direction.RIGHT: (28, 0),
    }
    ATTACK_FRAME_INDEX: int = 1

    def __init__(self, x: int, y: int,
                 start_x: int,
                 end_x: int,
                 ) -> None:
        super().__init__(x, y, start_x, end_x)
        self._anim_rect: Rect = self.rect
        self.go_frames_counter: FramesCounter = FramesCounter(
            frames_count=len(SkeletonImages.GO_RIGHT),
            transition_delay_as_seconds=self.GO_ANIM_DELAY,
        )
        self.attack_frames_counter: FramesCounter = FramesCounter(
            frames_count=len(SkeletonImages.ATTACK_RIGHT),
            transition_delay_as_seconds=self.ATTACK_ANIM_DELAY,
        )
        self.attack_direction: Direction | None = None

    def _move(self) -> None:
        if self.attack_frames_counter.is_end:
            super()._move()

    def _handle_collision_with_player(self) -> None:
        if self.attack_frames_counter.current_index == self.ATTACK_FRAME_INDEX:
            super()._handle_collision_with_player()
        if self.attack_frames_counter.is_end:
            self.attack_frames_counter.is_end = False
            if self.map.player.rect.centerx < self.rect.centerx:
                self.attack_direction = Direction.LEFT
            elif self.map.player.rect.centerx >= self.rect.centerx:
                self.attack_direction = Direction.RIGHT

    def _update_image(self) -> None:
        if self.attack_frames_counter.is_end:
            self._anim_rect = self.rect
            if self.x_vel < 0:
                self.image = SkeletonImages.GO_LEFT[self.go_frames_counter.current_index]
            elif self.x_vel > 0:
                self.image = SkeletonImages.GO_RIGHT[self.go_frames_counter.current_index]
            self.go_frames_counter.next()
        else:
            if self.attack_direction == Direction.LEFT:
                self.image = SkeletonImages.ATTACK_LEFT[self.attack_frames_counter.current_index]
            elif self.attack_direction == Direction.RIGHT:
                self.image = SkeletonImages.ATTACK_RIGHT[self.attack_frames_counter.current_index]
            self._update_anim_rect_for_attack()
            self.attack_frames_counter.next()

    def _update_anim_rect_for_attack(self) -> None:
        self._anim_rect = Rect(
            self.rect.x - self.ATTACK_ANIM_INDENTS[self.attack_direction][self.attack_frames_counter.current_index],
            0,
            self.image.get_width(),
            self.image.get_height(),
        )
        self._anim_rect.bottom = self.rect.bottom

    def _draw(self) -> None:
        screen.blit(self.image, self.map.camera.apply(self._anim_rect))
