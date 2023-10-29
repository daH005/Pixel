from game.assets.images import CHEST_IMAGES
from game.assets.levels import LevelsManager
from game.contrib.annotations import SizeTupleType
from game.contrib.counters import TimeCounter
from game.map_.map_ import Map
from game.map_.abstract_ui import AbstractInteractingWithPlayerMapObject
from game.map_.ui.coin import Coin
from game.map_.exceptions import MapObjectCannotBeCreated

__all__ = (
    'Chest',
)


@Map.add_object_type
class Chest(AbstractInteractingWithPlayerMapObject):
    size: SizeTupleType = CHEST_IMAGES[0].get_size()
    COINS_SPAWN_DELAY: float = 0.1
    DEFAULT_COUNT: int = 10

    def __init__(self, x: int, y: int,
                 id_: int, count: int | None = None,
                 ) -> None:
        if id_ in LevelsManager.current_level.uncreating_ids:
            raise MapObjectCannotBeCreated
        super().__init__(x, y)
        self.id = id_
        if count is None:
            count = self.DEFAULT_COUNT
        self.max_count = count
        self.spawned_count: int = 0
        self.coins_spawn_timer: TimeCounter = TimeCounter(self.COINS_SPAWN_DELAY)
        self.is_opened = False

    def update(self) -> None:
        super().update()
        if self.is_opened and self.spawned_count < self.max_count:
            if not self.coins_spawn_timer.is_work():
                self.coins_spawn_timer.restart()
                self.map.grid.add(self._new_coin())
                self.spawned_count += 1
            self.coins_spawn_timer.next()

    def _update_image(self) -> None:
        if self.is_opened:
            self.image = CHEST_IMAGES[1]
        else:
            self.image = CHEST_IMAGES[0]

    def _handle_collision_with_player(self) -> None:
        if not self.is_opened:
            self.is_opened = True
            self.map.uncreating_ids.append(self.id)

    def _new_coin(self) -> Coin:
        coin: Coin = Coin(self.rect.x, self.rect.y)
        coin.take()
        return coin
