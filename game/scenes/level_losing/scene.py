from engine.common.typing_ import XYTupleType
from engine.common.colors import Color
from engine.scenes.manager import ScenesManager
from game.assets.fonts import PixelFonts
from game.scenes.keys import SceneKey
from game.common.windows.building import TextWindowPartBuilder
from game.common.windows.windows import Button, TextWindow
from game.common.windows.rect_relative_position_names import RectRelativePositionName
from game.scenes.common import AbstractLevelEndingScene

__all__ = (
    'LevelLosingScene',
)


@ScenesManager.add(SceneKey.LEVEL_LOSING)
class LevelLosingScene(AbstractLevelEndingScene):

    def __init__(self, scenes_manager: ScenesManager) -> None:
        super().__init__(scenes_manager=scenes_manager)

        screen_center: XYTupleType = self._screen.get_rect().center
        self._restart_button: Button = Button(
            builder=TextWindowPartBuilder(
                text='Начать заново',
                w=300,
            ),
            x=screen_center[0],
            y=screen_center[1] - 5,
            position_name=RectRelativePositionName.MIDBOTTOM,
            hover_background_color=Color.GREEN,
            on_click=self._restart_button_on_click,
        )
        self._levels_menu_button: Button = Button(
            builder=TextWindowPartBuilder(
                text='В меню',
                w=300,
            ),
            x=screen_center[0],
            y=screen_center[1] + 5,
            position_name=RectRelativePositionName.MIDTOP,
            hover_background_color=Color.RED,
            on_click=self._levels_menu_button_on_click,
        )
        self._title_window: TextWindow = TextWindow(
            builder=TextWindowPartBuilder(
                text='Помер!',
                w=500,
                font=PixelFonts.LARGE,
                text_color=Color.RED,
            ),
            x=screen_center[0],
            y=self._restart_button.get_rect().top - 20,
            position_name=RectRelativePositionName.MIDBOTTOM,
        )

    def _restart_button_on_click(self) -> None:
        self._scenes_manager.switch_to(SceneKey.LEVEL).reset()

    def _levels_menu_button_on_click(self) -> None:
        self._scenes_manager.switch_to(SceneKey.LEVELS_MENU)

    def update(self) -> None:
        super().update()
        self._title_window.update()
        self._restart_button.update()
        self._levels_menu_button.update()
