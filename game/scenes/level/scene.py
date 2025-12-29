from pygame import Surface, KEYDOWN, K_ESCAPE
from pygame.event import Event

from engine.common.colors import Color
from engine.common.typing_ import XYTupleType
from engine.exceptions import PlayerWasNotCreated
from engine.map_.camera import Camera
from engine.map_.grid.grid import Grid
from engine.scenes.abstract_scene import AbstractScene
from engine.scenes.manager import ScenesManager
from game.assets.images import SUN_IMAGE
from game.assets.sounds import level_music
from game.assets.save import get_coins_count, set_coins_count
from game.map_ import Map
from game.map_.ui.coin import Coin
from game.map_.abstract_ui import AbstractItemToDisposableCollect
from game.map_.levels_extra_data_keys import LevelExtraDataKey
from game.scenes.keys import SceneKey
from game.scenes.level.ui import (
    Background,
    CloudManager,
    CoinCounterHUD,
    PlayerHPHUD,
)

__all__ = (
    'LevelScene',
)


@ScenesManager.add(SceneKey.LEVEL)
class LevelScene(AbstractScene):

    _SCENE_KEY_TO_SWITCH_ON_PLAYER_WAS_NOT_CREATED_EXCEPTION: SceneKey = SceneKey.LEVELS_MENU
    _BACKGROUND_COLOR: Color = Color.BLUE
    _SUN_XY: XYTupleType = (50, 50)
    _saved_screen: Surface

    def __init__(self, scenes_manager: ScenesManager) -> None:
        super().__init__(scenes_manager=scenes_manager)
        self._camera = Camera()
        self._grid = Grid(camera=self._camera)
        self._map = Map(
            camera=self._camera,
            grid=self._grid,
            levels_manager=self._scenes_manager.levels_manager,
        )

        self._background: Background = Background(camera=self._camera)
        self._clouds: CloudManager = CloudManager()
        self._coins_counter_hud: CoinCounterHUD = CoinCounterHUD()
        self._player_hp_hud: PlayerHPHUD = PlayerHPHUD(map_=self._map)

        self._need_to_save_screen_and_switch_to: SceneKey | None = None

    def reset(self) -> None:
        try:
            self._map.reset()
        except PlayerWasNotCreated:
            self._on_player_was_not_created_exception()
            return
        self._clouds.reset()

    def _on_player_was_not_created_exception(self) -> None:
        print('The level is invalid! The player cannot be created.')
        level_music.stop()
        self._scenes_manager.switch_to(self._SCENE_KEY_TO_SWITCH_ON_PLAYER_WAS_NOT_CREATED_EXCEPTION)

    def on_open(self) -> None:
        self._need_to_save_screen_and_switch_to = False
        level_music.play(-1)

    def on_close(self) -> None:
        level_music.stop()

    def _handle_event(self, event: Event) -> None:
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self._need_to_save_screen_and_switch_to = SceneKey.LEVEL_PAUSE

    def update(self) -> None:
        super().update()

        self._screen.fill(self._BACKGROUND_COLOR)
        self._screen.blit(SUN_IMAGE, self._SUN_XY)

        self._clouds.update()
        self._background.update()
        self._map.update()
        self._check_player_hp()
        self._check_level_completion()
        self._save_screen_and_switch_if_it_need()
        self._player_hp_hud.update()
        self._coins_counter_hud.update()

    def _check_player_hp(self) -> None:
        if self._map.player.hp <= 0:
            self._need_to_save_screen_and_switch_to = SceneKey.LEVEL_LOSING

    def _check_level_completion(self) -> None:
        if self._map.is_completed:
            self._save_coins()
            self._save_collected_ids()
            self._need_to_save_screen_and_switch_to = SceneKey.LEVEL_COMPLETION

    @staticmethod
    def _save_coins() -> None:
        set_coins_count(count=get_coins_count() + Coin.collected_count)  # type: ignore

    def _save_collected_ids(self) -> None:
        saved_collected_ids = self._scenes_manager.levels_manager.current_level.extra[LevelExtraDataKey.COLLECTED_ITEMS_IDS]
        new_collected_ids = [*saved_collected_ids, *AbstractItemToDisposableCollect.collected_ids]
        self._scenes_manager.levels_manager.current_level.update_extra_data(**{
            LevelExtraDataKey.COLLECTED_ITEMS_IDS: new_collected_ids,
        })

    def _save_screen_and_switch_if_it_need(self) -> None:
        if self._need_to_save_screen_and_switch_to:
            self._saved_screen = self._screen.copy()
            self._scenes_manager.switch_to(self._need_to_save_screen_and_switch_to)

    @property
    def saved_screen(self) -> Surface:
        return self._saved_screen
