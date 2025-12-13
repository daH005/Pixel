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
    'LevelCompletionScene',
)


@ScenesManager.add(SceneKey.LEVEL_COMPLETION)
class LevelCompletionScene(AbstractLevelEndingScene):

    def __init__(self, scenes_manager: ScenesManager) -> None:
        super().__init__(scenes_manager=scenes_manager)

        screen_center: XYTupleType = self._screen.get_rect().center
        self._next_level_button: Button = Button(
            builder=TextWindowPartBuilder(
                text='Следующий',
                w=300,
            ),
            x=screen_center[0],
            y=screen_center[1] - 5,
            position_name=RectRelativePositionName.MIDBOTTOM,
            hover_background_color=Color.GREEN,
            on_click=self._next_level_button_on_click,
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
                text='Уровень пройден!',
                w=500,
                font=PixelFonts.LARGE,
                text_color=Color.GREEN,
            ),
            x=screen_center[0],
            y=self._next_level_button.get_rect().top - 20,
            position_name=RectRelativePositionName.MIDBOTTOM,
        )

    def _next_level_button_on_click(self) -> None:
        self._scenes_manager.levels_manager.go_next()
        self._scenes_manager.switch_to(SceneKey.LEVEL).reset()

    def _levels_menu_button_on_click(self) -> None:
        self._scenes_manager.switch_to(SceneKey.LEVELS_MENU)

    def update(self) -> None:
        super().update()
        self._title_window.update()
        self._next_level_button.update()
        self._levels_menu_button.update()
