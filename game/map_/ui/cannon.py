from engine.common.counters import FramesCounter
from engine.common.float_rect import FloatRect
from engine.common.direction import Direction
from engine.map_.map_ import Map
from game.assets.images import CannonImages
from game.assets.sounds import cannon_sound
from game.map_.abstract_ui import AbstractMapObject, AbstractMovingAndInteractingWithPlayerMapObject

__all__ = (
    'Cannon',
)


@Map.add_object_type
class Cannon(AbstractMapObject):

    _IMAGES = CannonImages
    _ANIMATION_DELAY: float = 0.4

    def __init__(self, map_: Map,
                 x: int, y: int,
                 end_x: int,
                 ) -> None:
        super().__init__(
            map_=map_,
            rect=self._IMAGES.DEFAULT_RIGHT.get_rect(x=x, y=y),
        )
        self._end_x = end_x

        if self._end_x < self._rect.centerx:
            self._images = self._IMAGES.SHOOT_LEFT
            self._cannonballs_spawn_x = self._rect.left
        else:
            self._images = self._IMAGES.SHOOT_RIGHT
            self._cannonballs_spawn_x: int = self._rect.right - self._IMAGES.CannonballImages.DEFAULT.get_width()

        self._shoot_frames_counter: FramesCounter = FramesCounter(
            frames_count=len(self._IMAGES.SHOOT_RIGHT),
            transition_delay_as_seconds=self._ANIMATION_DELAY,
        )

        self._shoot_frame_index: int = 3
        self._cannonball_spawn_y_indent: int = 10
        self._cannonballs: list[Cannonball] = []
        self._cannonball_was_spawned: bool = False

    def update(self) -> None:
        super().update()
        self._update_cannonballs()

    def _update_image(self) -> None:
        self._image = self._images[self._shoot_frames_counter.current_index]
        self._shoot_frames_counter.next()

    def _update_cannonballs(self) -> None:
        if self._shoot_frames_counter.current_index == self._shoot_frame_index:
            if not self._cannonball_was_spawned:
                cannon_sound.play()
                self._cannonballs.append(self._new_cannonball())
            self._cannonball_was_spawned = True
        else:
            self._cannonball_was_spawned = False
        for cannonball in self._cannonballs[:]:
            cannonball.update()
            if cannonball.to_delete:
                self._cannonballs.remove(cannonball)

    def _new_cannonball(self) -> 'Cannonball':
        return Cannonball(
            map_=self._map,
            x=self._cannonballs_spawn_x,
            y=self._rect.y + self._cannonball_spawn_y_indent,
            end_x=self._end_x,
        )


class Cannonball(AbstractMovingAndInteractingWithPlayerMapObject):

    _START_SPEED: float = 15
    _END_SPEED: float = 10
    _SPEED_DECREASE: float = 0.25
    _X_PUSHING_POWER: int = 20

    _IMAGES = CannonImages.CannonballImages
    _DEATH_ANIMATION_DELAY: float = 0.01

    def __init__(self, map_: Map,
                 x: int, y: int,
                 end_x: int,
                 ) -> None:
        self._image = self._IMAGES.DEFAULT
        super().__init__(
            map_=map_,
            rect=FloatRect(self._image.get_rect(x=x, y=y)),
        )
        self._end_x = end_x

        self._death_frames_counter: FramesCounter = FramesCounter(
            frames_count=len(self._IMAGES.DEATH),
            transition_delay_as_seconds=self._DEATH_ANIMATION_DELAY,
        )

        if end_x < self._rect.centerx:
            self._direction = Direction.LEFT
        else:
            self._direction: Direction = Direction.RIGHT

        self._current_speed: float = self._START_SPEED

    def update(self) -> None:
        super().update()
        if self._direction == Direction.RIGHT:
            if self._rect.right >= self._end_x:
                self._death_frames_counter.start()
        if self._direction == Direction.LEFT:
            if self._rect.left <= self._end_x:
                self._death_frames_counter.start()

    def _move(self) -> None:
        if self._death_frames_counter.is_end:
            self._rect.float_x += self._current_speed * self._direction.value
            self._decrease_speed()

    def _decrease_speed(self) -> None:
        if self._current_speed > self._END_SPEED:
            self._current_speed -= self._SPEED_DECREASE

    def _on_collision_with_player(self) -> None:
        self._map.player.hit(
            x_pushing=self._X_PUSHING_POWER,
            enemy_center_x=self._rect.centerx,
        )
        self._death_frames_counter.start()

    def _update_image(self) -> None:
        if not self._death_frames_counter.is_end:
            self._image = self._IMAGES.DEATH[self._death_frames_counter.current_index]
            self._death_frames_counter.next()
            if self._death_frames_counter.is_end:
                self._to_delete = True
