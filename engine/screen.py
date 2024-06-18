from pygame import init as init_pygame, Surface, display

__all__ = (
    'set_global_screen',
)

init_pygame()


def set_global_screen(h: int,
                      title: str,
                      flags: int,
                      icon: Surface,
                      ) -> None:
    display.set_mode(_prepare_window_size(h), flags=flags)
    display.set_caption(title)
    display.set_icon(icon)


def _prepare_window_size(h: int) -> tuple[int, int]:
    return _calc_window_w(h), h


def _calc_window_w(h: int) -> int:
    screen_info = display.Info()
    return int(h * (screen_info.current_w / screen_info.current_h))
