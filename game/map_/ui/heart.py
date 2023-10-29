from game.assets.images import HEART_IMAGES
from game.assets.sounds import heart_sound
from game.contrib.counters import FramesCounter
from game.contrib.annotations import SizeTupleType
from game.map_.map_ import Map
from game.map_.abstract_ui import AbstractInteractingWithPlayerMapObject

__all__ = (
    'Heart',
)


@Map.add_object_type
class Heart(AbstractInteractingWithPlayerMapObject):
    size: SizeTupleType = HEART_IMAGES[0].get_size()
    ANIM_DELAY: float = 1

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y)
        self.frames_counter: FramesCounter = FramesCounter(
            frames_count=len(HEART_IMAGES),
            transition_delay_as_seconds=self.ANIM_DELAY,
        )

    def _update_image(self) -> None:
        self.image = HEART_IMAGES[self.frames_counter.current_index]
        self.frames_counter.next()

    def _handle_collision_with_player(self) -> None:
        if self.map.player.hp < self.map.player.MAX_HP:
            self.to_delete = True
            self.map.player.relpenish_hp()
            heart_sound.play()
