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

    def __init__(self, map_: Map,
                 x: int, y: int,
                 start_x: int,
                 end_x: int,
                 ) -> None:
        super().__init__(
            map_=map_,
            rect=FloatRect(BatImages.GO_RIGHT[0].get_rect(x=x, y=y)),
            start_x=start_x,
            end_x=end_x,
            speed=2,
            x_pushing_power=15,
            y_pushing_power=-5,
        )
        self.go_frames_counter: FramesCounter = FramesCounter(
            frames_count=len(BatImages.GO_RIGHT),
            transition_delay_as_seconds=0.05,
        )

    def _update_image(self) -> None:
        if self._x_vel > 0:
            self._image = BatImages.GO_RIGHT[self.go_frames_counter.current_index]
        elif self._x_vel < 0:
            self._image = BatImages.GO_LEFT[self.go_frames_counter.current_index]
        self.go_frames_counter.next()
