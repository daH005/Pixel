from engine.common.colors import Color
from engine.common.typing_ import XYTupleType
from engine.scenes.manager import ScenesManager
from engine.scenes.abstract_scene import AbstractScene
from engine.exceptions import ExitFromGame
from game.assets.sounds import play_mainscreen_music
from game.assets.fonts import PixelFonts
from game.common.windows.building import TextWindowPartsSurfacesBuilder
from game.common.windows.windows import TextWindow, Button
from game.common.windows.rect_relative_position_names import RectRelativePositionName
from game.scenes.keys import SceneKey
from game.scenes.common import HomeBackground

__all__ = (
    'HomeScene',
)


@ScenesManager.add(SceneKey.HOME)
class HomeScene(AbstractScene):

    def __init__(self, scenes_manager: ScenesManager) -> None:
        super().__init__(scenes_manager=scenes_manager)
        self._background: HomeBackground = HomeBackground()

        screen_center: XYTupleType = self._screen.get_rect().center
        self._start_button: Button = Button(
            builder=TextWindowPartsSurfacesBuilder(
                text='Играть',
                w=300,
            ),
            x=screen_center[0],
            y=screen_center[1] - 5,
            position_name=RectRelativePositionName.MIDBOTTOM,
            hover_background_color=Color.GREEN,
            on_click=self._start_button_on_click,
        )
        self._exit_button: Button = Button(
            builder=TextWindowPartsSurfacesBuilder(
                text='Выйти',
                w=300,
            ),
            x=screen_center[0],
            y=screen_center[1] + 5,
            position_name=RectRelativePositionName.MIDTOP,
            hover_background_color=Color.RED,
            on_click=self._exit_button_on_click,
        )
        self._title_window: TextWindow = TextWindow(
            builder=TextWindowPartsSurfacesBuilder(
                text='Pixel',
                w=500,
                font=PixelFonts.LARGE,
            ),
            x=screen_center[0],
            y=self._start_button.get_rect().top - 20,
            position_name=RectRelativePositionName.MIDBOTTOM,
        )

    def _start_button_on_click(self) -> None:
        self._scenes_manager.switch_to(SceneKey.LEVELS_MENU)

    def _exit_button_on_click(self) -> None:
        raise ExitFromGame

    def on_open(self) -> None:
        play_mainscreen_music()

    def update(self) -> None:
        super().update()
        self._background.update()
        self._title_window.update()
        self._start_button.update()
        self._exit_button.update()
