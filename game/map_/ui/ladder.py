from pygame import Surface

from game.map_.abstract_ui import AbstractInteractingWithPlayerMapObject
from game.map_.map_ import Map
from game.contrib.annotations import SizeTupleType
from game.assets.images import LADDER_IMAGE

__all__ = (
    'Ladder',
)


@Map.add_object_type
class Ladder(AbstractInteractingWithPlayerMapObject):
    image: Surface = LADDER_IMAGE
    size: SizeTupleType = image.get_size()

    def _handle_collision_with_player(self) -> None:
        self.map.player.on_ladder = True
