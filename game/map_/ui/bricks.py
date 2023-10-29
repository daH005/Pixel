from pygame import Surface

from game.map_.abstract_ui import AbstractBlock, AbstractBackground
from game.map_.map_ import Map
from game.contrib.annotations import SizeTupleType
from game.assets.images import BricksImages

__all__ = (
    'Bricks',
    'BackgroundBricks',
)


@Map.add_object_type
class Bricks(AbstractBlock):
    image: Surface = BricksImages.DEFAULT
    size: SizeTupleType = image.get_size()


@Map.add_object_type
class BackgroundBricks(AbstractBackground):
    image: Surface = BricksImages.BACKGROUND
    size: SizeTupleType = image.get_size()
