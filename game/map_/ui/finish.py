from pygame import Surface

from game.map_.abstract_ui import AbstractInteractingWithPlayerMapObject
from game.map_.map_ import Map
from game.assets.images import FINISH_IMAGE
from game.contrib.annotations import SizeTupleType

__all__ = (
    'Finish',
)


@Map.add_object_type
class Finish(AbstractInteractingWithPlayerMapObject):
    image: Surface = FINISH_IMAGE
    size: SizeTupleType = image.get_size()

    def _handle_collision_with_player(self) -> None:
        self.map.finish()
