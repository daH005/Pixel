from abc import ABC

from game.contrib.exceptions import Exit
from game.assets.fonts import FontSize
from game.assets.sounds import play_mainscreen_music
from game.contrib.colors import Color
from game.contrib.windows import AbstractTextWindow, AbstractButton
from game.scenes.base import ScenesManager, AbstractScene, SceneKey
from game.config import GameConfig
from game.contrib.screen import SCREEN_RECT
from game.scenes.common_ui import HomeBackground

__all__ = (
    'HomeScene',
)


@ScenesManager.add(SceneKey.HOME)
class HomeScene(AbstractScene):
    """Начальный экран игры.
    По задумке располагает кирпичным фоном и двумя кнопками:
    "Уровни" и "Выйти".
    """

    Background = HomeBackground

    class TitleWindow(AbstractTextWindow):
        text: str = GameConfig.WINDOW_TITLE
        W: int = 500
        INNER_INDENT: int = 40
        FONT_SIZE: FontSize = FontSize.LARGE
        BOTTOM_Y_INDENT: int = 20

        def __init__(self, bottom_y: int) -> None:
            super().__init__()
            self.rect.centerx = SCREEN_RECT.centerx
            self.rect.bottom = bottom_y - self.BOTTOM_Y_INDENT

    class ButtonMixin(AbstractButton, ABC):
        BOTTOM_Y_INDENT: int = 5
        W: int = 300

    class StartButton(ButtonMixin):
        text: str = 'Уровни'
        HOVER_BACKGROUND_COLOR: Color = Color.GREEN

        def __init__(self) -> None:
            super().__init__()
            self.rect.centerx = SCREEN_RECT.centerx
            self.rect.bottom = SCREEN_RECT.centery - self.BOTTOM_Y_INDENT

        def on_click(self) -> None:
            ScenesManager.switch(SceneKey.LEVELS_MENU)

    class ExitButton(ButtonMixin):
        text: str = 'Выйти'
        HOVER_BACKGROUND_COLOR: Color = Color.RED

        def __init__(self) -> None:
            super().__init__()
            self.rect.centerx = SCREEN_RECT.centerx
            self.rect.top = SCREEN_RECT.centery + self.BOTTOM_Y_INDENT

        def on_click(self) -> None:
            raise Exit

    def __init__(self) -> None:
        self.background = self.Background()
        self.start_button = self.StartButton()
        self.exit_button = self.ExitButton()
        self.title_window = self.TitleWindow(self.start_button.rect.top)

    def on_switch(self) -> None:
        play_mainscreen_music()

    def _update(self) -> None:
        self.background.update()
        self.title_window.update()
        self.start_button.update()
        self.exit_button.update()
