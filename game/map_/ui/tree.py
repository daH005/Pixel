from pygame import Surface

from game.map_.abstract_ui import AbstractBackground
from game.map_.map_ import Map
from game.assets.images import TREES_IMAGES
from game.contrib.annotations import SizeTupleType

__all__ = (
    'Tree',
)


@Map.add_object_type
class Tree(AbstractBackground):
    Z_INDEX: int = -3

    def __init__(self, x: int, y: int,
                 image_index: int = 0,
                 ) -> None:
        self.image: Surface = TREES_IMAGES[image_index]
        self.size: SizeTupleType = self.image.get_size()
        super().__init__(x, y)
