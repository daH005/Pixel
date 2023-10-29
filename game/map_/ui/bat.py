from game.assets.images import BatImages
from game.contrib.counters import FramesCounter
from game.contrib.annotations import SizeTupleType
from game.map_.map_ import Map
from game.map_.abstract_ui import AbstractXPatrolEnemy

__all__ = (
    'Bat',
)


@Map.add_object_type
class Bat(AbstractXPatrolEnemy):
    size: SizeTupleType = BatImages.GO_RIGHT[0].get_size()
    SPEED: float = 2
    X_PUSHING_POWER: float = 15
    Y_PUSHING_POWER: float = -5

    GO_ANIM_DELAY: float = 0.05

    def __init__(self, x: int, y: int,
                 start_x: int,
                 end_x: int,
                 ) -> None:
        super().__init__(x, y, start_x, end_x)
        self.go_frames_counter: FramesCounter = FramesCounter(
            frames_count=len(BatImages.GO_RIGHT),
            transition_delay_as_seconds=self.GO_ANIM_DELAY,
        )

    def _update_image(self) -> None:
        if self.x_vel > 0:
            self.image = BatImages.GO_RIGHT[self.go_frames_counter.current_index]
        elif self.x_vel < 0:
            self.image = BatImages.GO_LEFT[self.go_frames_counter.current_index]
        self.go_frames_counter.next()
