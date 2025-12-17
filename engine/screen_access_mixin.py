from pygame import display, Surface

__all__ = (
    'ScreenAccessMixin',
)


class ScreenAccessMixin:

    @classmethod
    @property
    def _screen(cls) -> Surface:
        return display.get_surface()
