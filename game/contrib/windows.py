from __future__ import annotations
from pygame import mouse, Rect, Surface, SRCALPHA
from pygame.draw import rect as draw_rect
from pygame.font import Font
from abc import ABC, abstractmethod

from game.assets.fonts import PIXEL_FONTS, FontSize
from game.contrib.colors import Color, ColorTupleType
from game.contrib.annotations import SizeTupleType
from game.contrib.abstract_ui import AbstractUI

__all__ = (
    'WindowImagesBuilder',
    'AbstractWindow',
    'AbstractTextWindow',
    'AbstractButton',
)


class WindowImagesBuilder:
    """Построитель графических элементов пиксельного окна:
    - `new_text_surface()` - создаёт прозрачную поверхность с текстом.
    Текст может переноситься с помощью '\n'.
    - `new_background_surface(...)` - создаёт фоновую поверхность
    с прозрачными отступами по краям, выделяющимися под обрамление.
    - `new_border_surface(...)` - создаёт обводку окна.
    - `new_window_image(...)` - формирует полноценное окно.
    """

    def __init__(self, window: AbstractWindow) -> None:
        self.window = window
        self.FONT: Font = PIXEL_FONTS[self.window.FONT_SIZE]

    def new_text_surface(self) -> Surface:
        if '\n' in self.window.text:
            # Будем вычислять размеры итоговой поверхности по мере составления текстовых поверхностей.
            w: int = 0
            h: int = 0
            # Текстовые поверхности будем класть сюда:
            texts_surfaces: list[Surface] = []
            for i, text_part in enumerate(self.window.text.split('\n')):
                txt_surf: Surface = self.FONT.render(text_part, 0, self.window.DEFAULT_TEXT_COLOR)
                texts_surfaces.append(txt_surf)
                h += txt_surf.get_height()
                if i != 0:
                    h += self.window.NEW_STRING_TOP_INDENT
                w = max(w, txt_surf.get_width())
            # Итоговая поверхность (не забываем заполнить её начальным белым цветом).
            result_surf: Surface = Surface((w, h))
            result_surf.fill(Color.WHITE)
            # Рисуем построчно текст на итоговой поверхности, после чего возвращаем результат.
            y: int = 0
            for i, txt_surf in enumerate(texts_surfaces):
                result_surf.blit(txt_surf, (0, y))
                y += txt_surf.get_height() + self.window.NEW_STRING_TOP_INDENT
            return result_surf
        else:
            return self.FONT.render(self.window.text, 0, self.window.DEFAULT_TEXT_COLOR)

    def calc_window_size(self, text_surface: Surface) -> SizeTupleType:
        w: int
        if self.window.W is not None:
            w = self.window.W
        else:
            w = text_surface.get_width()
        h: int = text_surface.get_height()
        return tuple(map(lambda x: x + self.window.INNER_INDENT + self.window.BORDER_WH * 2, (w, h)))  # type: ignore

    @staticmethod
    def calc_text_center_rect(background_surface: Surface,
                              text_surface: Surface,
                              ) -> Rect:
        surface_rect: Rect = text_surface.get_rect()
        surface_rect.center = background_surface.get_rect().center
        return surface_rect

    def new_background_surface(self, background_color: ColorTupleType,
                               window_size: SizeTupleType,
                               ) -> Surface:
        background_surface: Surface = Surface(window_size, flags=SRCALPHA)
        draw_rect(
            background_surface,
            background_color,
            (
                self.window.BORDER_WH,
                self.window.BORDER_WH,
                window_size[0] - self.window.BORDER_WH * 2,
                window_size[1] - self.window.BORDER_WH * 2,
            )
        )
        return background_surface

    def new_border_surface(self, window_size: SizeTupleType) -> Surface:
        surface: Surface = Surface(window_size, flags=SRCALPHA)
        border_parts_rects: list[Rect] = [
            Rect(
                self.window.BORDER_WH,
                self.window.BORDER_WH,
                self.window.BORDER_WH,
                self.window.BORDER_WH
            ),
            Rect(
                self.window.BORDER_WH * 2,
                0,
                window_size[0] - self.window.BORDER_WH * 4,
                self.window.BORDER_WH
            ),
            Rect(
                window_size[0] - self.window.BORDER_WH * 2,
                self.window.BORDER_WH,
                self.window.BORDER_WH,
                self.window.BORDER_WH
            ),
            Rect(
                window_size[0] - self.window.BORDER_WH,
                self.window.BORDER_WH * 2,
                self.window.BORDER_WH,
                window_size[1] - self.window.BORDER_WH * 4
            ),
            Rect(
                window_size[0] - self.window.BORDER_WH * 2,
                window_size[1] - self.window.BORDER_WH * 2,
                self.window.BORDER_WH,
                self.window.BORDER_WH
            ),
            Rect(
                self.window.BORDER_WH * 2,
                window_size[1] - self.window.BORDER_WH,
                window_size[0] - self.window.BORDER_WH * 4,
                self.window.BORDER_WH
            ),
            Rect(
                self.window.BORDER_WH,
                window_size[1] - self.window.BORDER_WH * 2,
                self.window.BORDER_WH,
                self.window.BORDER_WH
            ),
            Rect(
                0,
                self.window.BORDER_WH * 2,
                self.window.BORDER_WH,
                window_size[1] - self.window.BORDER_WH * 4
            ),
        ]
        for rect in border_parts_rects:
            draw_rect(surface, Color.BLACK, rect)
        return surface

    def new_window_image(self, background_color: ColorTupleType,
                         window_size: SizeTupleType,
                         text_surface: Surface,
                         border_surface: Surface,
                         ) -> Surface:
        window_image: Surface = self.new_background_surface(background_color, window_size)
        window_image.blit(text_surface, self.calc_text_center_rect(window_image, text_surface))
        window_image.blit(border_surface, (0, 0))
        return window_image


class AbstractWindow(AbstractUI, ABC):
    DEFAULT_X: int = 0
    DEFAULT_Y: int = 0
    DEFAULT_BACKGROUND_COLOR: ColorTupleType = Color.WHITE
    DEFAULT_TEXT_COLOR: ColorTupleType = Color.BLACK
    text: str
    INNER_INDENT: int = 20
    W: int | None = None
    # Длина и ширина каждого пиксельного квадрата обводки.
    BORDER_WH: int = 4
    # Отступ между текстовыми строками.
    NEW_STRING_TOP_INDENT: int = 5
    FONT_SIZE: FontSize = FontSize.DEFAULT

    def __init__(self) -> None:
        self.images_builder = WindowImagesBuilder(self)
        self._init_temp_images()
        self._build_images()

    def _init_temp_images(self) -> None:
        self.text_surface = self.images_builder.new_text_surface()
        self.window_size = self.images_builder.calc_window_size(self.text_surface)
        self.border_surface = self.images_builder.new_border_surface(self.window_size)

    @abstractmethod
    def _build_images(self) -> None:
        pass


class AbstractTextWindow(AbstractWindow, ABC):
    """Абстрактный класс текстового окна. Не предполагает никакого интерактива."""

    def __init__(self) -> None:
        super().__init__()
        self.rect = Rect((self.DEFAULT_X, self.DEFAULT_Y) + self.image.get_size())

    def _build_images(self) -> None:
        self.image = self.images_builder.new_window_image(
            self.DEFAULT_BACKGROUND_COLOR,
            self.window_size,
            self.text_surface,
            self.border_surface,
        )


class AbstractButton(AbstractWindow, ABC):
    """Абстрактный класс кнопки. Изменяет цвет фона при наведении.
    При клике вызывается метод `on_click()`.
    """

    HOVER_BACKGROUND_COLOR: ColorTupleType = Color.GRAY
    default_image: Surface
    hover_image: Surface

    def __init__(self) -> None:
        super().__init__()
        self.rect = Rect((self.DEFAULT_X, self.DEFAULT_Y) + self.default_image.get_size())
        self.is_clicked: bool = False
        # Флаг для отслеживания того, что клик был произведён вне кнопки.
        self.is_pressed: bool = False

    def _build_images(self) -> None:
        self.default_image = self.images_builder.new_window_image(
            self.DEFAULT_BACKGROUND_COLOR,
            self.window_size,
            self.text_surface,
            self.border_surface,
        )
        self.hover_image = self.images_builder.new_window_image(
            self.HOVER_BACKGROUND_COLOR,
            self.window_size,
            self.text_surface,
            self.border_surface,
        )

    def update(self) -> None:
        self.image = self.default_image
        if self.rect.collidepoint(mouse.get_pos()):
            self.image = self.hover_image
            if mouse.get_pressed()[0] and not self.is_pressed:
                self.is_clicked = True
                self.on_click()
        self.is_pressed = False
        if mouse.get_pressed()[0]:
            self.is_pressed = True
        super().update()

    @abstractmethod
    def on_click(self) -> None:
        pass
