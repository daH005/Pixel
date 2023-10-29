from game.map_.abstract_ui import AbstractBlock
from game.map_.map_ import Map
from game.contrib.annotations import SizeTupleType

__all__ = (
    'InvisibleBarrier',
)


@Map.add_object_type
class InvisibleBarrier(AbstractBlock):
    size: SizeTupleType = (40, 40)

    def _draw(self) -> None: pass
