from pygame import display, Surface, Rect

__all__ = (
    'ScreenAccessMixin',
)


class ScreenAccessMixin:

    @classmethod
    @property
    def _screen(cls) -> Surface:
        return display.get_surface()
