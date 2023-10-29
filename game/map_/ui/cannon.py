from __future__ import annotations
from pygame import Surface

from game.assets.images import CannonImages
from game.assets.sounds import cannon_sound
from game.contrib.counters import FramesCounter
from game.contrib.annotations import SizeTupleType
from game.contrib.rects import FloatRect
from game.contrib.direction import Direction
from game.map_.map_ import Map
from game.map_.abstract_ui import AbstractMapObject, AbstractMovingAndInteractingWithPlayerMapObject

__all__ = (
    'Cannon',
)


@Map.add_object_type
class Cannon(AbstractMapObject):
    size: SizeTupleType = CannonImages.DEFAULT_RIGHT.get_size()
    SHOOT_ANIM_DELAY: float = 0.4
    SHOOT_FRAME_INDEX: int = 3
    CANNONBALL_SPAWN_Y_INDENT: int = 10

    def __init__(self, x: int, y: int,
                 end_x: int,
                 ) -> None:
        super().__init__(x, y)
        self.end_x = end_x
        self.IMAGES: list[Surface] = CannonImages.SHOOT_RIGHT
        self._cannonballs_spawn_x: int = self.rect.right - Cannonball.size[0]
        if self.end_x < self.rect.centerx:
            self.IMAGES = CannonImages.SHOOT_LEFT
            self._cannonballs_spawn_x = self.rect.left
        self.shoot_frames_counter: FramesCounter = FramesCounter(
            frames_count=len(CannonImages.SHOOT_RIGHT),
            transition_delay_as_seconds=self.SHOOT_ANIM_DELAY,
        )
        self.cannonballs: list[Cannonball] = []
        self.cannonball_was_spawned: bool = False

    def update(self) -> None:
        super().update()
        self._update_cannonballs()

    def _update_image(self) -> None:
        self.image = self.IMAGES[self.shoot_frames_counter.current_index]
        self.shoot_frames_counter.next()

    def _update_cannonballs(self) -> None:
        if self.shoot_frames_counter.current_index == self.SHOOT_FRAME_INDEX:
            if not self.cannonball_was_spawned:
                cannon_sound.play()
                self.cannonballs.append(self._new_cannonball())
            self.cannonball_was_spawned = True
        else:
            self.cannonball_was_spawned = False
        for cannonball in self.cannonballs[:]:
            cannonball.update()
            if cannonball.to_delete:
                self.cannonballs.remove(cannonball)

    def _new_cannonball(self) -> Cannonball:
        return Cannonball(self._cannonballs_spawn_x, self.rect.y + self.CANNONBALL_SPAWN_Y_INDENT, self.end_x)


class Cannonball(AbstractMovingAndInteractingWithPlayerMapObject):
    image: Surface = CannonImages.CannonballImages.DEFAULT
    size: SizeTupleType = CannonImages.CannonballImages.DEFAULT.get_size()
    RectType: type[FloatRect] = FloatRect

    DEATH_ANIM_DELAY: float = 0.01
    START_SPEED: float = 15
    END_SPEED: float = 10
    SPEED_DECREASE: float = 0.25

    def __init__(self, x: int, y: int, end_x: int) -> None:
        super().__init__(x, y)
        self.death_frames_counter: FramesCounter = FramesCounter(
            frames_count=len(CannonImages.CannonballImages.DEATH),
            transition_delay_as_seconds=self.DEATH_ANIM_DELAY,
        )
        self.end_x = end_x
        self.direction: Direction = Direction.RIGHT
        if end_x < self.rect.centerx:
            self.direction = Direction.LEFT
        self.cur_speed: float = self.START_SPEED

    def update(self) -> None:
        super().update()
        if self.direction == Direction.RIGHT:
            if self.rect.right >= self.end_x:
                self.death_frames_counter.is_end = False
        if self.direction == Direction.LEFT:
            if self.rect.left <= self.end_x:
                self.death_frames_counter.is_end = False

    def _move(self) -> None:
        if self.death_frames_counter.is_end:
            self.rect.float_x += self.cur_speed * self.direction  # type: ignore
            self._decrease_speed()

    def _decrease_speed(self) -> None:
        if self.cur_speed > self.END_SPEED:
            self.cur_speed -= self.SPEED_DECREASE

    def _handle_collision_with_player(self) -> None:
        self.map.player.hit()
        self.death_frames_counter.is_end = False

    def _update_image(self) -> None:
        if not self.death_frames_counter.is_end:
            self.image = CannonImages.CannonballImages.DEATH[self.death_frames_counter.current_index]
            self.death_frames_counter.next()
            if self.death_frames_counter.is_end:
                self.to_delete = True
