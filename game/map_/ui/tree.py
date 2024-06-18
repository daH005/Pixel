from pygame import Surface

from engine.map_.map_ import Map
from game.map_.abstract_ui import AbstractBackground
from game.assets.images import TREES_IMAGES

__all__ = (
    'Tree',
)


@Map.add_object_type
class Tree(AbstractBackground):

    def __init__(self, map_: Map,
                 x: int, y: int,
                 image_index: int = 0,
                 ) -> None:
        self._image: Surface = TREES_IMAGES[image_index]
        super().__init__(
            map_=map_,
            rect=self._image.get_rect(x=x, y=y),
            z_index=-3,
        )
