from game.assets.fonts import FontSize
from game.assets.levels import LevelsManager
from game.assets.sounds import mainscreen_music, play_mainscreen_music
from game.contrib.colors import Color
from game.contrib.windows import AbstractTextWindow, AbstractButton
from game.scenes.base import ScenesManager, AbstractScene, SceneKey
from game.contrib.screen import SCREEN_W, SCREEN_H
from game.scenes.home import HomeScene
from game.contrib.counters import TimeCounter

__all__ = (
    'LevelsMenuScene',
)

SCREEN_BORDER_INDENT: int = 10


@ScenesManager.add(SceneKey.LEVELS_MENU)
class LevelsMenuScene(AbstractScene):
    """Сцена со списком пронумерованных уровней.
    По задумке здесь располагаются кнопки, соответствующие уровням,
    а также кнопка для возврата на `MainScreenScene`.
    """

    Background = HomeScene.Background

    class BackButton(AbstractButton):
        text: str = 'Вернуться'
        FONT_SIZE: FontSize = FontSize.SMALL

        def __init__(self) -> None:
            super().__init__()
            self.rect.x = SCREEN_BORDER_INDENT
            self.rect.bottom = SCREEN_H - SCREEN_BORDER_INDENT

        def on_click(self) -> None:
            ScenesManager.switch(SceneKey.HOME)

    class LevelButton(AbstractButton):
        DEFAULT_Y: int = SCREEN_BORDER_INDENT
        W: int = 60
        INNER_INDENT: int = 10
        FONT_SIZE: FontSize = FontSize.LARGE
        RIGHT_X_INDENT: int = 10

        def __init__(self, level_index: int, x: int) -> None:
            self.level_index: int = level_index
            self.text = str(self.level_index + 1)
            super().__init__()
            self.rect.x = x

        def on_click(self) -> None:
            LevelsManager.change(self.level_index)
            ScenesManager.switch(SceneKey.LEVEL).reset()
            mainscreen_music.stop()

    class NotAvailableLevelButton(LevelButton):
        DEFAULT_BACKGROUND_COLOR: Color = Color.GRAY
        ALPHA: int = 180

        def __init__(self, level_index: int, x: int) -> None:
            super().__init__(level_index, x)
            self.default_image.set_alpha(self.ALPHA)
            self.hover_image.set_alpha(self.ALPHA)

        def on_click(self) -> None:
            ScenesManager.current_scene.level_not_available_window.counter.restart()

    class CurrentLevelButton(LevelButton):
        DEFAULT_BACKGROUND_COLOR: Color = Color.GREEN

    class LevelNotAvailableWindow(AbstractTextWindow):
        text: str = 'Сначала пройдите предыдущий уровень!'
        FONT_SIZE: FontSize = FontSize.SMALL
        VISIBILITY_DURATION: int = 5

        def __init__(self) -> None:
            super().__init__()
            self.rect.right = SCREEN_W - SCREEN_BORDER_INDENT
            self.rect.bottom = SCREEN_H - SCREEN_BORDER_INDENT
            self.counter = TimeCounter(self.VISIBILITY_DURATION)

        def update(self):
            self.counter.next()
            if self.counter.is_work():
                super().update()

    def __init__(self) -> None:
        self.background = self.Background()
        self.back_button = self.BackButton()
        self.level_not_available_window = self.LevelNotAvailableWindow()
        self.levels_buttons: list[LevelsMenuScene.LevelButton] = []

    def on_switch(self) -> None:
        self._reset_levels_buttons()
        self.level_not_available_window.counter.stop()
        play_mainscreen_music()

    def _reset_levels_buttons(self) -> None:
        self.levels_buttons.clear()
        x: int = SCREEN_BORDER_INDENT
        for i, level in enumerate(LevelsManager.LEVELS):
            button_type = self.LevelButton
            if not level.is_available:
                button_type = self.NotAvailableLevelButton
            if LevelsManager.current_level_on_list() == level:
                button_type = self.CurrentLevelButton
            button = button_type(level.index, x)
            self.levels_buttons.append(button)
            x = button.rect.right + button.RIGHT_X_INDENT

    def _update(self) -> None:
        self.background.update()
        self.back_button.update()
        for level_button in self.levels_buttons:
            level_button.update()
        self.level_not_available_window.update()
