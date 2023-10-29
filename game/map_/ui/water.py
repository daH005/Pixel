from pygame import Surface

from game.map_.map_ import Map
from game.map_.abstract_ui import AbstractInteractingWithPlayerMapObject
from game.assets.images import WaterImages
from game.contrib.annotations import SizeTupleType

__all__ = (
    'Water',
)


@Map.add_object_type
class Water(AbstractInteractingWithPlayerMapObject):
    Z_INDEX: int = 6

    def __init__(self, x: int, y: int,
                 is_top: bool = False,
                 ):
        if is_top:
            self.image: Surface = WaterImages.TOP
        else:
            self.image: Surface = WaterImages.DEFAULT
        self.size: SizeTupleType = self.image.get_size()
        super().__init__(x, y)

    def _handle_collision_with_player(self) -> None:
        self.map.player.in_water = True
