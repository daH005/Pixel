from functools import partial
from typing import Callable

from engine.common.counters import TimeCounter
from engine.common.typing_ import XYTupleType, ColorTupleType
from engine.common.colors import Color
from engine.scenes.manager import ScenesManager
from engine.scenes.abstract_scene import AbstractScene
from game.assets.sounds import play_mainscreen_music, mainscreen_music
from game.assets.fonts import PixelFonts
from game.common.windows.building import TextWindowPartsSurfacesBuilder
from game.common.windows.windows import Button, TextWindow
from game.common.windows.rect_relative_position_names import RectRelativePositionName
from game.scenes.keys import SceneKey
from game.scenes.common import HomeBackground

__all__ = (
    'LevelsMenuScene',
)


@ScenesManager.add(SceneKey.LEVELS_MENU)
class LevelsMenuScene(AbstractScene):
    _SCREEN_BORDER_INDENT: int = 10

    def __init__(self, scenes_manager: ScenesManager) -> None:
        super().__init__(scenes_manager=scenes_manager)
        self._background: HomeBackground = HomeBackground()

        screen_bottomleft: XYTupleType = self._screen.get_rect().bottomleft
        self._back_button: Button = Button(
            builder=TextWindowPartsSurfacesBuilder(
                text='Вернуться',
                font=PixelFonts.SMALL,
            ),
            x=screen_bottomleft[0] + self._SCREEN_BORDER_INDENT,
            y=screen_bottomleft[1] - self._SCREEN_BORDER_INDENT,
            position_name=RectRelativePositionName.BOTTOMLEFT,
            hover_background_color=Color.RED,
            on_click=self._back_button_on_click,
        )

        screen_bottomright: XYTupleType = self._screen.get_rect().bottomright
        self._not_available_level_message_window: TextWindow = TextWindow(
            builder=TextWindowPartsSurfacesBuilder(
                text='Сначала пройдите предыдущий уровень!',
                font=PixelFonts.SMALL,
            ),
            x=screen_bottomright[0] - self._SCREEN_BORDER_INDENT,
            y=screen_bottomright[1] - self._SCREEN_BORDER_INDENT,
            position_name=RectRelativePositionName.BOTTOMRIGHT,
        )
        self._not_available_level_message_counter = TimeCounter(5)

        self._levels_buttons: list[Button] = []

    def _back_button_on_click(self) -> None:
        self._scenes_manager.switch_to(SceneKey.HOME)

    def on_open(self) -> None:
        self._reset_levels_buttons()
        self._not_available_level_message_counter.stop()
        play_mainscreen_music()

    def _reset_levels_buttons(self) -> None:
        self._levels_buttons.clear()

        x: int = self._SCREEN_BORDER_INDENT
        for i, level in enumerate(self._scenes_manager.levels_manager.levels):

            button_factory = self._new_completed_level_button
            if not level.is_available:
                button_factory = self._new_not_available_level_button
            if self._scenes_manager.levels_manager.current_level_by_list() == level:
                button_factory = self._new_current_level_button

            button = button_factory(text=str(level.index), level_index=level.index, x=x)
            self._levels_buttons.append(button)

            x = button.get_rect().right + 10

    def _new_completed_level_button(self, text: str,
                                    level_index: int,
                                    x: int,
                                    ) -> Button:
        return self._new_abstract_level_button(
            text=text,
            x=x,
            on_click=partial(self._available_level_button_on_click, level_index=level_index),
        )

    def _new_current_level_button(self, text: str,
                                  level_index: int,
                                  x: int,
                                  ) -> Button:
        return self._new_abstract_level_button(
            text=text,
            x=x,
            default_background_color=Color.GREEN,
            on_click=partial(self._available_level_button_on_click, level_index=level_index),
        )

    def _available_level_button_on_click(self, level_index: int) -> None:
        self._scenes_manager.levels_manager.switch_to(level_index)
        self._scenes_manager.switch_to(SceneKey.LEVEL).reset()
        mainscreen_music.stop()

    def _new_not_available_level_button(self, text: str,
                                        level_index: int,  # noqa
                                        x: int,
                                        ) -> Button:
        return self._new_abstract_level_button(
            text=text,
            x=x,
            default_background_color=Color.GRAY,
            alpha=180,
            on_click=self._not_available_level_button_on_click,
        )

    def _not_available_level_button_on_click(self) -> None:
        self._not_available_level_message_counter.restart()

    def _new_abstract_level_button(self, text: str,
                                   x: int,
                                   on_click: Callable,
                                   default_background_color: ColorTupleType = Color.WHITE,
                                   alpha: int | None = None,
                                   ) -> Button:
        return Button(
            builder=TextWindowPartsSurfacesBuilder(
                text=text,
                font=PixelFonts.LARGE,
                w=60,
                inner_indent=5,
            ),
            x=x,
            y=self._SCREEN_BORDER_INDENT,
            default_background_color=default_background_color,
            alpha=alpha,
            on_click=on_click,
        )

    def update(self) -> None:
        super().update()
        self._background.update()
        self._back_button.update()

        for level_button in self._levels_buttons:
            level_button.update()

        if self._not_available_level_message_counter.is_working():
            self._not_available_level_message_window.update()
            self._not_available_level_message_counter.next()
