from engine.map_.map_ import Map
from engine.common.counters import FramesCounter
from engine.common.float_rect import FloatRect
from game.assets.images import BatImages
from game.map_.abstract_ui import AbstractXPatrolEnemy

__all__ = (
    'Bat',
)


@Map.add_object_type
class Bat(AbstractXPatrolEnemy):

    _SPEED = 2
    _X_PUSHING_POWER = 15
    _Y_PUSHING_POWER = -5

    _IMAGES = BatImages
    _ANIMATION_DELAY: float = 0.05

    def __init__(self, map_: Map,
                 x: int, y: int,
                 start_x: int,
                 end_x: int,
                 ) -> None:
        super().__init__(
            map_=map_,
            rect=FloatRect(self._IMAGES.GO_RIGHT[0].get_rect(x=x, y=y)),
            start_x=start_x,
            end_x=end_x,
        )
        self._go_frames_counter: FramesCounter = FramesCounter(
            frames_count=len(self._IMAGES.GO_RIGHT),
            transition_delay_as_seconds=self._ANIMATION_DELAY,
        )

    def _update_image(self) -> None:
        if self._x_vel > 0:
            self._image = self._IMAGES.GO_RIGHT[self._go_frames_counter.current_index]
        elif self._x_vel < 0:
            self._image = self._IMAGES.GO_LEFT[self._go_frames_counter.current_index]
        self._go_frames_counter.next()
