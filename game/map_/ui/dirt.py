from pygame import Surface

from game.map_.abstract_ui import AbstractBlock, AbstractBackground
from game.map_.map_ import Map
from game.assets.images import DirtImages
from game.contrib.annotations import SizeTupleType
from game.contrib.direction import Direction

__all__ = (
    'Dirt',
    'BackgroundDirt',
)


@Map.add_object_type
class Dirt(AbstractBlock):
    size: SizeTupleType = DirtImages.DEFAULT.get_size()
    grass_index: int = 0

    EDGES_IMAGES: dict[Direction, Surface] = {
        Direction.LEFT: DirtImages.LEFT,
        Direction.RIGHT: DirtImages.RIGHT,
    }

    def __init__(self, x: int, y: int,
                 direction: Direction | None = None,
                 grass_enabled: bool = False,
                 ) -> None:
        super().__init__(x, y)
        self.image: Surface
        if direction is not None:
            self.image = self.EDGES_IMAGES[direction].copy()
        else:
            self.image = DirtImages.DEFAULT.copy()
        if grass_enabled:
            self.image.blit(DirtImages.GRASS_LIST[self.grass_index], (0, 0))
            self._increment_grass_index()

    @classmethod
    def _increment_grass_index(cls) -> None:
        cls.grass_index += 1
        if cls.grass_index > len(DirtImages.GRASS_LIST) - 1:
            cls.grass_index = 0


@Map.add_object_type
class BackgroundDirt(AbstractBackground):
    image: Surface = DirtImages.BACKGROUND
    size: SizeTupleType = image.get_size()
