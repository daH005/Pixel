from pygame.font import Font
from pygame import Surface, Rect, SRCALPHA
from pygame.draw import rect as draw_rect

from engine.common.colors import Color
from engine.common.typing_ import ColorTupleType, SizeTupleType
from game.assets.fonts import PixelFonts

__all__ = (
    'TextWindowPartsSurfacesBuilder',
)


class TextWindowPartsSurfacesBuilder:

    def __init__(self, text: str,
                 font: Font = PixelFonts.MEDIUM,
                 w: int | None = None,
                 border_wh: int = 4,
                 inner_indent: int = 20,
                 text_color: ColorTupleType = Color.BLACK,
                 ) -> None:
        self._text = text
        self._font = font
        self._w = w
        self._border_wh = border_wh
        self._inner_indent = inner_indent
        self._text_color = text_color

    def new_text_surface(self, new_string_top_indent: int = 5) -> Surface:
        if '\n' in self._text:
            # Будем вычислять размеры итоговой поверхности по мере составления текстовых поверхностей.
            w: int = 0
            h: int = 0
            # Текстовые поверхности будем класть сюда:
            texts_surfaces: list[Surface] = []
            for i, text_part in enumerate(self._text.split('\n')):
                txt_surf: Surface = self._font.render(text_part, 0, self._text_color)
                texts_surfaces.append(txt_surf)
                h += txt_surf.get_height()
                if i != 0:
                    h += new_string_top_indent
                w = max(w, txt_surf.get_width())
            # Итоговая поверхность (не забываем заполнить её начальным белым цветом).
            result_surf: Surface = Surface((w, h))
            result_surf.fill(Color.WHITE)
            # Рисуем построчно текст на итоговой поверхности, после чего возвращаем результат.
            y: int = 0
            for i, txt_surf in enumerate(texts_surfaces):
                result_surf.blit(txt_surf, (0, y))
                y += txt_surf.get_height() + new_string_top_indent
            return result_surf
        else:
            return self._font.render(self._text, 0, self._text_color)

    def calc_window_size(self, text_surface: Surface) -> SizeTupleType:
        w: int
        if self._w is not None:
            w = self._w
        else:
            w = text_surface.get_width()
        h: int = text_surface.get_height()
        return tuple(map(lambda x: x + self._inner_indent + self._border_wh * 2, (w, h)))  # type: ignore

    @staticmethod
    def calc_text_center_rect(background_surface: Surface,
                              text_surface: Surface,
                              ) -> Rect:
        surface_rect: Rect = text_surface.get_rect()
        surface_rect.center = background_surface.get_rect().center
        return surface_rect

    def new_background_surface(self, window_size: SizeTupleType,
                               background_color: ColorTupleType = Color.WHITE,
                               ) -> Surface:
        background_surface: Surface = Surface(window_size, flags=SRCALPHA)
        draw_rect(
            background_surface,
            background_color,
            (
                self._border_wh,
                self._border_wh,
                window_size[0] - self._border_wh * 2,
                window_size[1] - self._border_wh * 2,
            )
        )
        return background_surface

    def new_border_surface(self, window_size: SizeTupleType) -> Surface:
        surface: Surface = Surface(window_size, flags=SRCALPHA)
        border_parts_rects: list[Rect] = [
            Rect(
                self._border_wh,
                self._border_wh,
                self._border_wh,
                self._border_wh
            ),
            Rect(
                self._border_wh * 2,
                0,
                window_size[0] - self._border_wh * 4,
                self._border_wh
            ),
            Rect(
                window_size[0] - self._border_wh * 2,
                self._border_wh,
                self._border_wh,
                self._border_wh
            ),
            Rect(
                window_size[0] - self._border_wh,
                self._border_wh * 2,
                self._border_wh,
                window_size[1] - self._border_wh * 4
            ),
            Rect(
                window_size[0] - self._border_wh * 2,
                window_size[1] - self._border_wh * 2,
                self._border_wh,
                self._border_wh
            ),
            Rect(
                self._border_wh * 2,
                window_size[1] - self._border_wh,
                window_size[0] - self._border_wh * 4,
                self._border_wh
            ),
            Rect(
                self._border_wh,
                window_size[1] - self._border_wh * 2,
                self._border_wh,
                self._border_wh
            ),
            Rect(
                0,
                self._border_wh * 2,
                self._border_wh,
                window_size[1] - self._border_wh * 4
            ),
        ]
        for rect in border_parts_rects:
            draw_rect(surface, Color.BLACK, rect)
        return surface

    def new_window_image(self, window_size: SizeTupleType,
                         text_surface: Surface,
                         border_surface: Surface,
                         background_color: ColorTupleType = Color.WHITE,
                         ) -> Surface:
        window_image: Surface = self.new_background_surface(window_size, background_color)
        window_image.blit(text_surface, self.calc_text_center_rect(window_image, text_surface))
        window_image.blit(border_surface, (0, 0))
        return window_image
