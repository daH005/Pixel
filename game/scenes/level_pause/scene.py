from pygame import KEYDOWN, K_ESCAPE
from pygame.event import Event

from engine.common.colors import Color
from engine.common.typing_ import XYTupleType
from engine.scenes.manager import ScenesManager
from game.common.windows.building import TextWindowPartsSurfacesBuilder
from game.common.windows.windows import Button
from game.common.windows.rect_relative_position_names import RectRelativePositionName
from game.scenes.keys import SceneKey
from game.scenes.common import AbstractLevelOverlayScene


__all__ = (
    'LevelPauseScene',
)


@ScenesManager.add(SceneKey.LEVEL_PAUSE)
class LevelPauseScene(AbstractLevelOverlayScene):

    def __init__(self, scenes_manager: ScenesManager) -> None:
        super().__init__(scenes_manager=scenes_manager)

        screen_center: XYTupleType = self._screen.get_rect().center
        self._restart_button: Button = Button(
            builder=TextWindowPartsSurfacesBuilder(
                text='Начать заново',
                w=300,
            ),
            x=screen_center[0],
            y=screen_center[1],
            position_name=RectRelativePositionName.CENTER,
            hover_background_color=Color.GOLD,
            on_click=self._restart_button_on_click,
        )
        self._continue_button: Button = Button(
            builder=TextWindowPartsSurfacesBuilder(
                text='Продолжить',
                w=300,
            ),
            x=screen_center[0],
            y=self._restart_button.get_rect().top - 10,
            position_name=RectRelativePositionName.MIDBOTTOM,
            hover_background_color=Color.GREEN,
            on_click=self._continue_button_on_click,
        )
        self._levels_menu_button: Button = Button(
            builder=TextWindowPartsSurfacesBuilder(
                text='В меню',
                w=300,
            ),
            x=screen_center[0],
            y=self._restart_button.get_rect().bottom + 10,
            position_name=RectRelativePositionName.MIDTOP,
            hover_background_color=Color.RED,
            on_click=self._levels_menu_button_on_click,
        )

    def _restart_button_on_click(self) -> None:
        self._scenes_manager.switch_to(SceneKey.LEVEL).reset()

    def _continue_button_on_click(self) -> None:
        self._scenes_manager.switch_to(SceneKey.LEVEL)

    def _levels_menu_button_on_click(self) -> None:
        self._scenes_manager.switch_to(SceneKey.LEVELS_MENU)

    def _handle_event(self, event: Event) -> None:
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self._scenes_manager.switch_to(SceneKey.LEVEL)

    def update(self) -> None:
        super().update()

        self._continue_button.update()
        self._levels_menu_button.update()
        self._restart_button.update()
