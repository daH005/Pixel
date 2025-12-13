from pygame import mouse, Rect
from abc import abstractmethod
from typing import Callable

from engine.common.colors import Color
from engine.common.typing_ import ColorTupleType
from engine.abstract_ui import AbstractRectangularUI
from game.common.windows.building import TextWindowPartBuilder
from game.common.windows.rect_relative_position_names import RectRelativePositionName

__all__ = (
    'AbstractTextWindow',
    'TextWindow',
    'Button',
)


class AbstractTextWindow(AbstractRectangularUI):

    def __init__(self, builder: TextWindowPartBuilder,
                 x: int = 0, y: int = 0,
                 position_name: RectRelativePositionName = RectRelativePositionName.TOPLEFT,
                 ) -> None:
        self._builder = builder
        self._init_temp_images()
        self._build_images()

        rect: Rect = Rect(0, 0, *self._window_size)
        setattr(rect, position_name, (x, y))
        super().__init__(rect=rect)

    def _init_temp_images(self) -> None:
        self._text_surface = self._builder.new_text_surface()
        self._window_size = self._builder.calc_window_size(self._text_surface)
        self._border_surface = self._builder.new_border_surface(self._window_size)

    @abstractmethod
    def _build_images(self) -> None:
        pass


class TextWindow(AbstractTextWindow):

    def __init__(self, builder: TextWindowPartBuilder,
                 x: int = 0, y: int = 0,
                 position_name: RectRelativePositionName = RectRelativePositionName.TOPLEFT,
                 background_color: ColorTupleType = Color.WHITE,
                 alpha: int | None = None,
                 ) -> None:
        self._background_color = background_color
        super().__init__(builder=builder, x=x, y=y, position_name=position_name)
        if alpha:
            self._image.set_alpha(alpha)

    def _build_images(self) -> None:
        self._image = self._builder.new_window_image(
            self._window_size,
            self._text_surface,
            self._border_surface,
            self._background_color,
        )


class Button(AbstractTextWindow):

    def __init__(self, builder: TextWindowPartBuilder,
                 on_click: Callable,
                 x: int = 0, y: int = 0,
                 position_name: RectRelativePositionName = RectRelativePositionName.TOPLEFT,
                 default_background_color: ColorTupleType = Color.WHITE,
                 hover_background_color: ColorTupleType = Color.GRAY,
                 alpha: int | None = None
                 ) -> None:
        self._default_background_color = default_background_color
        self._hover_background_color = hover_background_color
        super().__init__(builder=builder, x=x, y=y, position_name=position_name)
        if alpha:
            self._default_image.set_alpha(alpha)
            self._hover_image.set_alpha(alpha)

        self._is_pressed_on_other_area: bool = False
        self._on_click = on_click

    def _build_images(self) -> None:
        self._default_image = self._builder.new_window_image(
            self._window_size,
            self._text_surface,
            self._border_surface,
            self._default_background_color,
        )
        self._hover_image = self._builder.new_window_image(
            self._window_size,
            self._text_surface,
            self._border_surface,
            self._hover_background_color,
        )

    def update(self) -> None:
        self._image = self._default_image
        if self._rect.collidepoint(mouse.get_pos()):
            self._image = self._hover_image

            if mouse.get_pressed()[0] and not self._is_pressed_on_other_area:
                self._on_click()

        self._is_pressed_on_other_area = False
        if mouse.get_pressed()[0]:
            self._is_pressed_on_other_area = True

        super().update()
