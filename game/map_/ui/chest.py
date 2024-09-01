from engine.map_.map_ import Map
from engine.common.counters import TimeCounter
from game.assets.images import CHEST_IMAGES
from game.map_.abstract_ui import AbstractItemToDisposableCollect
from game.map_.ui.coin import Coin

__all__ = (
    'Chest',
)


@Map.add_object_type
class Chest(AbstractItemToDisposableCollect):
    _DEFAULT_COINS_COUNT: int = 10

    def __init__(self, map_: Map,
                 x: int, y: int,
                 id_: int, count: int | None = None,
                 ) -> None:
        super().__init__(
            map_=map_,
            rect=CHEST_IMAGES[0].get_rect(x=x, y=y),
            id_=id_,
        )

        if count is None:
            count = self._DEFAULT_COINS_COUNT

        self._max_count = count
        self._spawned_count: int = 0
        self._coins_spawn_delay_timer: TimeCounter = TimeCounter(0.1)
        self._is_opened = False

    def update(self) -> None:
        super().update()
        if self._is_opened and self._spawned_count < self._max_count:
            if not self._coins_spawn_delay_timer.is_working():
                self._coins_spawn_delay_timer.restart()
                self._map.grid.add(self._new_coin())
                self._spawned_count += 1
            self._coins_spawn_delay_timer.next()

    def _update_image(self) -> None:
        if self._is_opened:
            self._image = CHEST_IMAGES[1]
        else:
            self._image = CHEST_IMAGES[0]

    def _handle_collision_with_player(self) -> None:
        if not self._is_opened:
            self._is_opened = True
            self.take()

    def _new_coin(self) -> Coin:
        coin: Coin = Coin(
            map_=self._map,
            x=self._rect.x,
            y=self._rect.y,
        )
        coin.take()
        return coin
