from engine.map_.map_ import Map
from game.map_.abstract_ui import AbstractBlock, AbstractBackground
from game.assets.images import BricksImages

__all__ = (
    'Bricks',
    'BackgroundBricks',
)


@Map.add_object_type
class Bricks(AbstractBlock):

    def __init__(self, map_: Map,
                 x: int, y: int,
                 ) -> None:
        self._image = BricksImages.DEFAULT
        super().__init__(
            map_=map_,
            rect=self._image.get_rect(x=x, y=y),
        )


@Map.add_object_type
class BackgroundBricks(AbstractBackground):

    def __init__(self, map_: Map,
                 x: int, y: int,
                 ) -> None:
        self._image = BricksImages.BACKGROUND
        super().__init__(
            map_=map_,
            rect=self._image.get_rect(x=x, y=y),
        )
